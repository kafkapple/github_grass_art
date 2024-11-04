from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ReadmeGenerator:
    def __init__(self, template_path="templates/README_template.md"):
        self.template_path = Path(template_path)
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
        
        logger.info(f"Initialized ReadmeGenerator with template: {template_path}")

    def format_preview_section(self, preview_files):
        """Format preview section with all styles"""
        preview_content = ""
        
        for style, preview_file in sorted(preview_files.items()):
            preview_content += f"### {style.capitalize()} Style\n```\n"
            
            try:
                with open(preview_file, 'r', encoding='utf-8') as f:
                    preview_content += f.read().strip()
            except Exception as e:
                logger.error(f"Error reading preview file {preview_file}: {e}")
                preview_content += f"Error loading preview for {style} style"
            
            preview_content += "\n```\n\n"
        
        return preview_content.strip()

    def generate(self, preview_files, selected_style, schedule_info):
        """Generate README content"""
        try:
            # Prepare all the template variables
            template_vars = {
                'generation_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'preview_results': self.format_preview_section(preview_files),
                'selected_style': selected_style,
                'total_commits': schedule_info['total_commits'],
                'start_date': schedule_info['start_date'].strftime("%Y-%m-%d"),
                'end_date': schedule_info['end_date'].strftime("%Y-%m-%d")
            }
            
            # Fill the template
            new_content = self.template.format(**template_vars)
            
            # Read existing README.md content
            readme_path = Path("README.md")
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            else:
                existing_content = "# GitHub Grass Art\n\n"
            
            # Append new content to existing content
            updated_content = existing_content + "\n" + new_content
            
            # Write updated content to README.md
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info("Successfully updated README.md")
            
        except Exception as e:
            logger.error(f"Error generating README: {e}")
            raise