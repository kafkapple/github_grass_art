# image_processor.py

from PIL import Image, ImageDraw, ImageFont
import numpy as np

class ImageProcessor:
    def __init__(self, input_data, is_text=True):
        self.input_data = input_data
        self.is_text = is_text
        self.width = 52  # GitHub 잔디 그래프의 너비 (주)
        self.height = 7  # GitHub 잔디 그래프의 높이 (요일)
        self.pixel_data = None

    def process(self):
        if self.is_text:
            image = self.text_to_image(self.input_data)
        else:
            image = self.load_image(self.input_data)
        image = self.resize_image(image)
        self.pixel_data = self.image_to_pixels(image)
        return self.pixel_data

    def text_to_image(self, text):
        font_size = 100
        font = ImageFont.truetype("arial.ttf", font_size)
        # 텍스트 크기에 맞게 이미지 생성
        text_width, text_height = font.getsize(text)
        image = Image.new('RGB', (text_width, text_height), color='white')
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, fill='black', font=font)
        return image

    def load_image(self, image_path):
        image = Image.open(image_path).convert('RGB')
        return image

    def resize_image(self, image):
        image = image.resize((self.width, self.height), Image.NEAREST)
        return image

    def image_to_pixels(self, image):
        image = image.convert('L')  # 흑백으로 변환
        pixels = np.array(image)
        # 흑백 임계값 적용
        threshold = 128
        pixels = (pixels < threshold).astype(int)
        return pixels  # 2D numpy 배열 (0 또는 1)