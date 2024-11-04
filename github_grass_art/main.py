import argparse
import logging
from pathlib import Path
import os
from .image_processor import ImageProcessor
from .preview_generator import PreviewGenerator
from .schedule_generator import ScheduleGenerator
from .auto_commit import AutoCommitter
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments or get interactive input"""
    parser = argparse.ArgumentParser(
        description='Create GitHub contribution graph art'
    )
    
    try:
        # Interactive mode if no command line arguments
        if len(os.sys.argv) == 1:
            logger.debug("Starting interactive mode")
            input_type = input("Select input type (1: Text, 2: Image file): ")
            
            if input_type == "1":
                input_data = input("Enter text: ")
                is_text = True
                logger.info(f"[INPUT] Text entered: '{input_data}'")
            else:
                input_data = input("Enter image file path: ")
                is_text = False
                logger.info(f"[INPUT] Image path entered: '{input_data}'")
            
            repo_path = input("Enter local repository path: ")
            logger.info(f"[INPUT] Repository path: '{repo_path}'")
            
            args = argparse.Namespace()
            args.input = input_data
            args.repo = repo_path
            args.is_text = is_text
            return args
        
        # Command line mode
        parser.add_argument('-t', '--text', help='Text to display')
        parser.add_argument('-i', '--image', help='Image file path')
        parser.add_argument('-r', '--repo', required=True, help='Local repository path')
        
        args = parser.parse_args()
        args.input = args.text if args.text else args.image
        args.is_text = bool(args.text)
        return args
        
    except Exception as e:
        logger.error(f"Error during argument parsing: {str(e)}")
        logger.debug(f"Detailed error:\n{traceback.format_exc()}")
        raise

def show_preview(pixel_data, style_name):
    """Show preview for a specific style"""
    logger.info(f"Generating preview for style: {style_name}")
    preview = PreviewGenerator(pixel_data)
    preview.generate_preview(style_name)

def main():
    try:
        args = parse_arguments()
        logger.info("GitHub Grass Art starting...")

        # 1. Image Processing - generate all styles
        logger.info("Processing image for all styles...")
        processor = ImageProcessor(args.input, is_text=args.is_text, style='simple')
        all_styles = processor.process_all_styles()

        # 2. Show previews for all styles
        logger.info("Generating previews for all styles...")
        for style_name, pixel_data in all_styles.items():
            print(f"\nPreview for {style_name.upper()} style:")
            show_preview(pixel_data, style_name)
            input("Press Enter to see next style...")

        # 3. Style selection
        while True:
            style_choice = input("\nSelect style (1: Simple, 2: Gradient, 3: Border): ")
            style_map = {'1': 'simple', '2': 'gradient', '3': 'border'}
            if style_choice in style_map:
                selected_style = style_map[style_choice]
                break
            print("Invalid choice. Please try again.")

        pixel_data = all_styles[selected_style]
        logger.info(f"Selected style: {selected_style}")

        # Final confirmation
        confirm = input("\nProceed with selected style? (y/n): ")
        if confirm.lower() != 'y':
            logger.info("Operation cancelled by user")
            return 0

        # 4. Generate commit schedule
        logger.info("Generating commit schedule...")
        scheduler = ScheduleGenerator(pixel_data)
        schedule = scheduler.generate_schedule()
        logger.info(f"Schedule generated with {len(schedule)} commits")

        # 5. Auto Commit
        logger.info("Starting auto commit process...")
        repo_path = Path(args.repo)
        if not repo_path.exists():
            logger.error(f"Repository path not found: {args.repo}")
            return 1

        committer = AutoCommitter(schedule, str(repo_path))
        committer.commit()
        committer.push()

        logger.info("All operations completed successfully!")
        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.debug(f"Detailed error stack:\n{traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    main() 