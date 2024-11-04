# preview_generator.py

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PreviewGenerator:
    def __init__(self, pixel_data):
        self.pixel_data = pixel_data
        self.colors = {
            0: '⬜',  # 배경
            1: '🟩',  # 연한 녹색
            2: '🟨',  # 중간 강도
            3: '🟧',  # 진한 강도
            4: '🟥',  # 가장 진한 강도
        }

    def generate_preview(self, output_path):
        """Generate ASCII art preview and save to file"""
        try:
            preview_str = ''
            for row in self.pixel_data:
                for cell in row:
                    preview_str += self.colors.get(cell, '⬜')
                preview_str += '\n'
            
            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(preview_str)
            
            logger.info(f"Preview saved to: {output_path}")
            return preview_str
            
        except Exception as e:
            logger.error(f"Error generating preview: {e}")
            raise