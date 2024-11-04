import argparse
import logging
from pathlib import Path
import os
from .image_processor import ImageProcessor
from .preview_generator import PreviewGenerator
from .schedule_generator import ScheduleGenerator
from .readme_generator import ReadmeGenerator
import traceback
from collections import Counter

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
                input_data = input("Enter text (default: 'bori'): ") or "bori"
                is_text = True
                logger.info(f"[INPUT] Text entered: '{input_data}'")
            else:
                input_data = input("Enter image file path (default: 'templates/1.png'): ") or "templates/1.png"
                is_text = False
                logger.info(f"[INPUT] Image path entered: '{input_data}'")
            
            args = argparse.Namespace()
            args.input = input_data
            args.is_text = is_text
            return args
        
        # Command line mode
        parser.add_argument('-t', '--text', help='Text to display')
        parser.add_argument('-i', '--image', help='Image file path')
        
        args = parser.parse_args()
        args.input = args.text if args.text else args.image
        args.is_text = bool(args.text)
        return args
        
    except Exception as e:
        logger.error(f"Error during argument parsing: {str(e)}")
        logger.debug(f"Detailed error:\n{traceback.format_exc()}")
        raise

def show_preview(pixel_data, output_path):
    """Show preview for a specific style and save to file"""
    logger.info(f"Generating preview for style: {output_path.stem}")
    preview = PreviewGenerator(pixel_data)
    preview.generate_preview(output_path)
    # Read and print the preview
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            preview_content = f.read()
            print(preview_content)
    except Exception as e:
        logger.error(f"Error reading preview file: {e}")

def save_schedule(schedule, output_path):
    """Save commit schedule to file"""
    try:
        with open(output_path, 'w') as f:
            f.write("GitHub Grass Art - Commit Schedule\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Style: {output_path.stem}\n")
            f.write(f"Total commits required: {len(schedule)}\n\n")
            
            # Group commits by date
            commit_counts = Counter(schedule)
            
            f.write("Daily Commit Schedule:\n")
            f.write("-" * 40 + "\n")
            for date, count in sorted(commit_counts.items()):
                f.write(f"{date.strftime('%Y-%m-%d (%A)')}: {count} commits\n")
        
        logger.info(f"Schedule saved to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error saving schedule: {str(e)}")
        raise

def setup_output_directory():
    """Set up output directory structure"""
    output_dir = Path("output")
    previews_dir = output_dir / "previews"
    schedules_dir = output_dir / "schedules"
    
    # Create directories if they don't exist
    for dir_path in [output_dir, previews_dir, schedules_dir]:
        dir_path.mkdir(exist_ok=True)
        
    logger.info(f"Created output directories in {output_dir}")
    return output_dir, previews_dir, schedules_dir

def main():
    try:
        args = parse_arguments()
        logger.info("GitHub Grass Art starting...")

        # Set up output directories
        output_dir, previews_dir, schedules_dir = setup_output_directory()

        # 1. Image Processing - generate all styles
        logger.info("Processing image for all styles...")
        processor = ImageProcessor(args.input, is_text=args.is_text, style='simple')
        all_styles = processor.process_all_styles()

        # 2. Show previews for all styles
        logger.info("Generating previews for all styles...")
        preview_files = {}
        for style_name, pixel_data in all_styles.items():
            print(f"\nPreview for {style_name.upper()} style:")
            
            # Save preview to output directory
            preview_file = previews_dir / f"preview_{style_name}.txt"
            show_preview(pixel_data, preview_file)
            preview_files[style_name] = preview_file
            
            # Generate and save schedule
            scheduler = ScheduleGenerator(pixel_data)
            schedule = scheduler.generate_schedule()
            schedule_file = schedules_dir / f"schedule_{style_name}.txt"
            save_schedule(schedule, schedule_file)
            
            print(f"\nPreview saved to: {preview_file}")
            print(f"Schedule saved to: {schedule_file}")
            print(f"Total commits required: {len(schedule)}")
            
            input("\nPress Enter to see next style...")

        # 3. Style selection
        while True:
            style_choice = input("\nSelect style (1: Simple, 2: Gradient, 3: Border): ")
            style_map = {'1': 'simple', '2': 'gradient', '3': 'border'}
            if style_choice in style_map:
                selected_style = style_map[style_choice]
                break
            print("Invalid choice. Please try again.")

        # 4. Update README with previews
        readme_gen = ReadmeGenerator()
        schedule_info = {
            'total_commits': len(schedule),
            'start_date': min(schedule),
            'end_date': max(schedule)
        }
        readme_gen.generate(preview_files, selected_style, schedule_info)

        logger.info(f"Selected style: {selected_style}")
        print(f"\nYou selected {selected_style.upper()} style.")
        print(f"\nOutput files are in:")
        print(f"- Previews: {previews_dir}")
        print(f"- Schedules: {schedules_dir}")
        print("\nPreview results have been added to README.md")
        
        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.debug(f"Detailed error stack:\n{traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    main()