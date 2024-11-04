# preview_generator.py

import numpy as np
from PIL import Image

class PreviewGenerator:
    def __init__(self, pixel_data):
        self.pixel_data = pixel_data
        self.colors = {
            0: '⬜',  # 흰색 (배경)
            1: '🟩',  # 연한 녹색
            2: '🟨',  # 중간 녹색을 노란색으로
            3: '🟧',  # 진한 녹색을 주황색으로
            4: '🟥',  # 가장 진한 녹색을 빨간색으로
        }

    def generate_preview(self, style_name='preview'):
        """Generate ASCII art preview and save to file"""
        preview_str = ''
        for row in self.pixel_data:
            for cell in row:
                preview_str += self.colors.get(cell, '⬜')
            preview_str += '\n'
        
        # Save to file with style name
        filename = f'preview_{style_name}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(preview_str)
        
        # Also print to console
        print(f"\nPreview saved to {filename}:")
        print(preview_str)