import argparse
import logging
import sys
import os
from src.youtube_processor.flow import create_youtube_processor_flow, create_file_processor_flow

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("youtube_processor.log")
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the content processor."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Process a YouTube video or a folder of documents to extract topics, questions, and generate ELI5 answers."
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--url", 
        type=str, 
        help="YouTube video URL to process"
    )
    group.add_argument(
        "--folder",
        type=str,
        help="Path to a folder with .txt and .pdf files to process"
    )

    parser.add_argument(
        "-v",
        "--vietnamese",
        action="store_true",
        help="Use Vietnamese for processing (default is English)",
    )
    args = parser.parse_args()
    
    # Initialize shared memory
    shared = {
        "language": "vietnamese" if args.vietnamese else "english",
    }
    
    # Determine the flow to run
    if args.folder:
        logger.info(f"Starting file content processor for folder: {args.folder}")
        flow = create_file_processor_flow()
        shared["folder_path"] = args.folder
    elif args.url:
        logger.info(f"Starting YouTube content processor for URL: {args.url}")
        flow = create_youtube_processor_flow()
        shared["url"] = args.url
    else:
        # Default behavior or prompt user
        url = input("Enter YouTube URL to process: ")
        logger.info(f"Starting YouTube content processor for URL: {url}")
        flow = create_youtube_processor_flow()
        shared["url"] = url

    logger.info(f"Language: {shared['language']}")

    # Run the flow
    flow.run(shared)
    
    output_file = shared.get("output_html_file", "output.html")
    
    # Report success and output file location
    print("\n" + "=" * 50)
    print("Processing completed successfully!")
    print(f"Output HTML file: {os.path.abspath(output_file)}")
    print("=" * 50 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
