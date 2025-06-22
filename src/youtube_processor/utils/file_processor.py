import os
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def process_folder(folder_path: str) -> dict:
    """
    Processes all .txt and .pdf files in a given folder.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        dict: A dictionary containing the concatenated text content,
              the folder name as the title, and the folder path as the URL.
              Returns an error dictionary if the path is invalid.
    """
    if not os.path.isdir(folder_path):
        error_msg = f"Provided path is not a valid directory: {folder_path}"
        logger.error(error_msg)
        return {"error": error_msg}

    all_text = ""
    for filename in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    all_text += f.read() + "\n\n"
                logger.info(f"Successfully read text file: {filename}")
            except Exception as e:
                logger.warning(f"Could not read text file {filename}: {e}")
        elif filename.lower().endswith(".pdf"):
            try:
                with fitz.open(file_path) as doc:
                    pdf_text = ""
                    for page in doc:
                        pdf_text += page.get_text()
                    all_text += pdf_text + "\n\n"
                logger.info(f"Successfully read PDF file: {filename}")
            except Exception as e:
                logger.warning(f"Could not read PDF file {filename}: {e}")

    if not all_text:
        logger.warning(f"No text could be extracted from the folder: {folder_path}")

    return {
        "transcript": all_text,
        "title": os.path.basename(folder_path),
        "url": folder_path,
        "thumbnail_url": "",  # No thumbnail for folder processing
        "video_id": "", # No video_id for folder processing
    }

def main():
    """Main function for testing the file processor."""
    # Create a dummy folder and files for testing
    if not os.path.exists("test_folder"):
        os.makedirs("test_folder")
    with open("test_folder/test1.txt", "w") as f:
        f.write("This is a test text file.")
    with open("test_folder/test2.txt", "w") as f:
        f.write("This is another test text file.")
    
    # You would need to manually add a PDF for a full test
    # For now, we just test with text files
    
    result = process_folder("test_folder")
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Title: {result['title']}")
        print(f"Transcript Length: {len(result['transcript'])}")
        print("--- Transcript ---")
        print(result['transcript'])

    # Clean up dummy files
    os.remove("test_folder/test1.txt")
    os.remove("test_folder/test2.txt")
    os.rmdir("test_folder")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main() 