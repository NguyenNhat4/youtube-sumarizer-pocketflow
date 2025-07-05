from typing import List, Dict, Any, Tuple
import yaml
import logging
import re
from pocketflow import Node, BatchNode, Flow
from .utils.call_llm import call_llm
from .utils.youtube_processor import get_video_info
from .utils.html_generator import html_generator
from .utils.file_processor import process_folder

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define the specific nodes for the YouTube Content Processor

class ProcessFolder(Node):
    """Process a folder to extract text content"""
    def prep(self, shared):
        """Get folder_path from shared"""
        return shared.get("folder_path", "")

    def exec(self, folder_path):
        """Extract text from all files in the folder"""
        if not folder_path:
            raise ValueError("No folder path provided")

        logger.info(f"Processing folder: {folder_path}")
        content_info = process_folder(folder_path)

        if "error" in content_info:
            raise ValueError(f"Error processing folder: {content_info['error']}")

        return content_info

    def post(self, shared, prep_res, exec_res):
        """Store content information in shared"""
        shared["video_info"] = exec_res # Re-use the same structure as video processing
        logger.info(f"Content title: {exec_res.get('title')}")
        logger.info(f"Content length: {len(exec_res.get('transcript', ''))}")
        return "default"

class ProcessYouTubeURL(Node):
    """Process YouTube URL to extract video information"""
    def prep(self, shared):
        """Get URL from shared"""
        return shared.get("url", "")
    
    def exec(self, url):
        """Extract video information"""
        if not url:
            raise ValueError("No YouTube URL provided")
        
        logger.info(f"Processing YouTube URL: {url}")
        video_info = get_video_info(url)
        
        if "error" in video_info:
            raise ValueError(f"Error processing video: {video_info['error']}")
        
        return video_info
    
    def post(self, shared, prep_res, exec_res):
        """Store video information in shared"""
        shared["video_info"] = exec_res
        logger.info(f"Video title: {exec_res.get('title')}")
        logger.info(f"Transcript length: {len(exec_res.get('transcript', ''))}")
        return "default"

class ExtractTopicsAndQuestions(Node):
    """Extract interesting topics and generate questions from the video transcript"""
    def prep(self, shared):
        """Get transcript and title from video_info"""
        video_info = shared.get("video_info", {})
        transcript = video_info.get("transcript", "")
        title = video_info.get("title", "")
        language = shared.get("language", "english")
        return {"transcript": transcript, "title": title, "language": language}
    
    def exec(self, data):
        """Extract topics and generate questions using LLM"""
        transcript = data["transcript"]
        title = data["title"]
        language = data["language"]
        
        if language == "vietnamese":
            prompt = f"""
Bạn là một chuyên gia phân tích nội dung. Với một bản ghi video YouTube, hãy xác định tối đa 5 chủ đề thú vị nhất được thảo luận và tạo ra thiểu 2 câu hỏi kích thích tư duy nhất cho mỗi chủ đề.
Những câu hỏi này không nhất thiết phải được hỏi trực tiếp trong video. Có thể là những câu hỏi làm rõ.

TIÊU ĐỀ VIDEO: {title}

BẢN GHI:
{transcript}

Định dạng phản hồi của bạn bằng YAML:

```yaml
topics:
  - title: |
        Tiêu đề chủ đề đầu tiên
    questions:
      - |
        Câu hỏi 1 về chủ đề đầu tiên?
      - |
        Câu hỏi 2 ...
  - title: |
        Tiêu đề chủ đề thứ hai
    questions:
        ...
```
"""
        else:
            prompt = f"""
You are an expert content analyzer. Given a YouTube video transcript, identify at most 5 most interesting topics discussed and generate at most 3 most thought-provoking questions for each topic.
These questions don't need to be directly asked in the video. It's good to have clarification questions.

VIDEO TITLE: {title}

TRANSCRIPT:
{transcript}

Format your response in YAML:

```yaml
topics:
  - title: |
        First Topic Title
    questions:
      - |
        Question 1 about first topic?
      - |
        Question 2 ...
  - title: |
        Second Topic Title
    questions:
        ...
```
"""
        
        response = call_llm(prompt)
        
        # Extract YAML content
        yaml_content = response.split("```yaml")[1].split("```")[0].strip() if "```yaml" in response else response
        

        parsed = yaml.safe_load(yaml_content)
        raw_topics = parsed.get("topics", [])
        
        # Ensure we have at most 5 topics
        raw_topics = raw_topics[:5]
        
        # Format the topics and questions for our data structure
        result_topics = []
        for topic in raw_topics:
            topic_title = topic.get("title", "")
            raw_questions = topic.get("questions", [])
            
            # Create a complete topic with questions
            result_topics.append({
                "title": topic_title,
                "questions": [
                    {
                        "original": q,
                        "rephrased": "",
                        "answer": ""
                    }
                    for q in raw_questions
                ]
            })
        
        return result_topics
    
    def post(self, shared, prep_res, exec_res):
        """Store topics with questions in shared"""
        shared["topics"] = exec_res
        
        # Count total questions
        total_questions = sum(len(topic.get("questions", [])) for topic in exec_res)
        
        logger.info(f"Extracted {len(exec_res)} topics with {total_questions} questions")
        return "default"

class ProcessContent(BatchNode):
    """Process each topic for rephrasing and answering"""
    def prep(self, shared):
        """Return list of topics for batch processing"""
        topics = shared.get("topics", [])
        video_info = shared.get("video_info", {})
        transcript = video_info.get("transcript", "")
        language = shared.get("language", "english")
        
        batch_items = []
        for topic in topics:
            batch_items.append({
                "topic": topic,
                "transcript": transcript,
                "language": language
            })
        
        return batch_items
    
    def exec(self, item):
        """Process a topic using LLM"""
        topic = item["topic"]
        transcript = item["transcript"]
        language = item["language"]
        
        # Truncate transcript to avoid token limits
        if len(transcript) > 100000:
            transcript = transcript[:100000]

        topic_title = topic["title"]
        questions = [q["original"] for q in topic["questions"]]
        
        if language == "vietnamese":
            prompt = f"""Bạn là một người đơn giản hóa nội dung cho trẻ em. Với một chủ đề và các câu hỏi từ video YouTube, hãy diễn đạt lại tiêu đề chủ đề và các câu hỏi để rõ ràng hơn, và cung cấp câu trả lời đơn giảnแบบ ELI5 (Giải thích như cho đứa trẻ 5 tuổi).

CHỦ ĐỀ: {topic_title}

CÂU HỎI:
{chr(10).join([f"- {q}" for q in questions])}

TRÍCH ĐOẠN BẢN GHI:
{transcript}

Đối với tiêu đề chủ đề và câu hỏi:
1. Giữ chúng hấp dẫn và thú vị, nhưng ngắn gọn

Đối với câu trả lời của bạn:
1. Định dạng chúng bằng HTML với các thẻ <b> và <i> để làm nổi bật.
2. Ưu tiên danh sách với các thẻ <ol> và <li>. Lý tưởng nhất là <li> theo sau bởi <b> cho các điểm chính.
3. Trích dẫn các từ khóa quan trọng nhưng giải thích chúng bằng ngôn ngữ dễ hiểu (ví dụ: "<b>Máy tính lượng tử</b> giống như có một chiếc máy tính ma thuật siêu nhanh")
4. Giữ câu trả lời thú vị nhưng ngắn gọn

Định dạng phản hồi của bạn bằng YAML:

```yaml
rephrased_title: |
    Tiêu đề chủ đề thú vị trong 10 từ
questions:
  - original: |
        {questions[0] if len(questions) > 0 else ''}
    rephrased: |
        Câu hỏi thú vị trong 15 từ
    answer: |
        Câu trả lời đơn giản mà một đứa trẻ 5 tuổi có thể hiểu trong 100 từ
  - original: |
        {questions[1] if len(questions) > 1 else ''}
    ...
```
"""
        else:
            prompt = f"""You are a content simplifier for children. Given a topic and questions from a YouTube video, rephrase the topic title and questions to be clearer, and provide simple ELI5 (Explain Like I'm 5) answers.

TOPIC: {topic_title}

QUESTIONS:
{chr(10).join([f"- {q}" for q in questions])}

TRANSCRIPT EXCERPT:
{transcript}

For topic title and questions:
1. Keep them catchy and interesting, but short

For your answers:
1. Format them using HTML with <b> and <i> tags for highlighting. 
2. Prefer lists with <ol> and <li> tags. Ideally, <li> followed by <b> for the key points.
3. Quote important keywords but explain them in easy-to-understand language (e.g., "<b>Quantum computing</b> is like having a super-fast magical calculator")
4. Keep answers interesting but short

Format your response in YAML:

```yaml
rephrased_title: |
    Interesting topic title in 10 words
questions:
  - original: |
        {questions[0] if len(questions) > 0 else ''}
    rephrased: |
        Interesting question in 15 words
    answer: |
        Simple answer that a 5-year-old could understand in 100 words
  - original: |
        {questions[1] if len(questions) > 1 else ''}
    ...
```
"""
        
        response = call_llm(prompt)
        
        # Extract YAML content
        yaml_content = response.split("```yaml")[1].split("```")[0].strip() if "```yaml" in response else response
        
        parsed = yaml.safe_load(yaml_content)
        rephrased_title = parsed.get("rephrased_title", topic_title)
        processed_questions = parsed.get("questions", [])
        
        result = {
            "title": topic_title,
            "rephrased_title": rephrased_title,
            "questions": processed_questions
        }
        
        return result

    
    def post(self, shared, prep_res, exec_res_list):
        """Update topics with processed content in shared"""
        
        # prep_res is the list of batch_items from prep()
        # exec_res_list is the list of results from exec()
        
        for item, processed_data in zip(prep_res, exec_res_list):
            topic = item["topic"] # This is a reference to a dictionary in shared["topics"]
            
            # Update the original topic with the new data
            topic["rephrased_title"] = processed_data.get("rephrased_title", "")
            
            processed_questions = processed_data.get("questions", [])
            
            for i, q_orig in enumerate(topic["questions"]):
                if i < len(processed_questions):
                    q_proc = processed_questions[i]
                    # The LLM might not return the 'original' field, so we just match by order
                    q_orig["rephrased"] = q_proc.get("rephrased", "")
                    q_orig["answer"] = q_proc.get("answer", "")

        logger.info(f"Processed content for {len(exec_res_list)} topics")
        return "default"

class GenerateHTML(Node):
    """Generate the final HTML output file"""
    def prep(self, shared):
        """Get all necessary data from shared"""
        video_info = shared.get("video_info", {})
        topics = shared.get("topics", [])
        output_title = shared.get("output_title") # Can be None
        
        # If no custom title, create one from the video/folder title
        if not output_title:
            base_title = video_info.get("title", "output")
            # Sanitize the title to be a valid filename
            output_title = re.sub(r'[\\/*?:"<>|]', "", base_title).replace(" ", "_")

        return {
            "title": video_info.get("title", ""),
            "url": video_info.get("url", ""),
            "thumbnail_url": video_info.get("thumbnail_url", ""),
            "video_id": video_info.get("video_id", ""),
            "topics": topics,
            "output_title": output_title # Pass the final title to exec and post
        }
    
    def exec(self, data):
        """Generate HTML content"""

        # Prepare sections for HTML generator
        sections = []
        for topic in data["topics"]:
            if not topic.get("questions"):
                continue
            
            section_title = topic.get("rephrased_title", topic.get("title", ""))
            
            bullets = []
            for question in topic.get("questions", []):
                q = question.get("rephrased", question.get("original", ""))
                a = question.get("answer", "")
                if q.strip() and a.strip():
                    bullets.append((q, a))
            
            if bullets:
                sections.append({
                    "title": section_title,
                    "bullets": bullets
                })

        html_content = html_generator(
            title=data["title"],
            image_url=data["thumbnail_url"],
            sections=sections
        )
        return {"html": html_content, "output_title": data["output_title"]}
    
    def post(self, shared, prep_res, exec_res):
        """Save the HTML content to a file"""
        html_content = exec_res["html"]
        output_title = exec_res["output_title"]
        
        output_filename = f"{output_title}.html"
        output_path = f"myoutput/current_output/{output_filename}"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        shared["output_html_file"] = output_path
        logger.info(f"Generated HTML report: {output_path}")
        return "default"

# Create the flow
def create_youtube_processor_flow():
    """Build and return the PocketFlow for YouTube processing."""
    
    # Create nodes
    process_youtube_url = ProcessYouTubeURL()
    extract_topics_questions = ExtractTopicsAndQuestions(max_retries=3)
    process_content = ProcessContent(max_retries=3)
    generate_html = GenerateHTML()

    # Define flow
    process_youtube_url >> extract_topics_questions >> process_content >> generate_html
    
    # Create and return flow
    return Flow(start=process_youtube_url)

def create_file_processor_flow():
    """Build and return the PocketFlow for file processing."""
    
    # Create nodes
    process_folder_node = ProcessFolder()
    extract_topics_questions = ExtractTopicsAndQuestions(max_retries=3)
    process_content = ProcessContent(max_retries=3)
    generate_html = GenerateHTML()

    # Define flow
    process_folder_node >> extract_topics_questions >> process_content >> generate_html
    
    # Create and return flow
    return Flow(start=process_folder_node)
