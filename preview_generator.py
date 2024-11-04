# preview_generator.py

import numpy as np
from PIL import Image

class PreviewGenerator:
    def __init__(self, pixel_data):
        self.pixel_data = pixel_data
        self.pixel_size = 20  # 미리보기 이미지에서 한 픽셀의 크기

    def generate_preview(self, output_path='preview.png'):
        height, width = self.pixel_data.shape
        image = Image.new('RGB', (width * self.pixel_size, height * self.pixel_size), 'white')
        pixels = image.load()

        for y in range(height):
            for x in range(width):
                color = (0, 180, 0) if self.pixel_data[y, x] == 1 else (235, 235, 235)
                for i in range(self.pixel_size):
                    for j in range(self.pixel_size):
                        pixels[x * self.pixel_size + i, y * self.pixel_size + j] = color

        image.save(output_path)
        print(f"미리보기 이미지가 {output_path}에 저장되었습니다.")