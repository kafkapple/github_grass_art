# image_processor.py

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import platform
import os
import logging
from scipy.ndimage import gaussian_filter

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, input_data, is_text=True, style='simple'):
        """
        Initialize ImageProcessor
        
        Args:
            input_data: Text string or image path
            is_text: Boolean indicating if input is text
            style: Rendering style ('simple', 'gradient', 'border')
        """
        self.input_data = input_data
        self.is_text = is_text
        self.style = style
        self.width = 52  # GitHub contribution graph width (weeks)
        self.height = 7  # GitHub contribution graph height (days)
        logger.info(f"Initialized ImageProcessor with style: {style}")

    def get_system_font(self):
        """Get system font path"""
        system = platform.system()
        if system == 'Darwin':  # macOS
            return '/System/Library/Fonts/AppleSDGothicNeo.ttc'
        elif system == 'Windows':
            return 'C:\\Windows\\Fonts\\arial.ttf'
        else:  # Linux
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/TTF/DejaVuSans.ttf'
            ]
            for path in font_paths:
                if os.path.exists(path):
                    return path
            return None

    def text_to_image(self, text):
        """Convert text to image"""
        try:
            width = 400
            height = 100
            background_color = 'white'
            text_color = 'black'
            font_size = 60
            
            font_path = self.get_system_font()
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
                
            image = Image.new('RGB', (width, height), background_color)
            draw = ImageDraw.Draw(image)
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            draw.text((x, y), text, font=font, fill=text_color)
            return image
            
        except Exception as e:
            logger.error(f"Error in text_to_image: {str(e)}")
            raise

    def process_all_styles(self):
        """Generate all style variations and return them"""
        if self.is_text:
            image = self.text_to_image(self.input_data)
        else:
            image = Image.open(self.input_data)

        styles = {
            'simple': self.process_style(image, 'simple'),
            'gradient': self.process_style(image, 'gradient'),
            'border': self.process_style(image, 'border')
        }
        
        logger.info("Generated all style variations")
        return styles

    def process_style(self, image, style):
        """Process image with specific style"""
        temp_style = self.style  # Store current style
        self.style = style      # Temporarily set style
        result = self.image_to_pixels(image)  # Process with this style
        self.style = temp_style  # Restore original style
        return result

    def process(self):
        """Main processing method - now returns the selected style"""
        styles = self.process_all_styles()
        return styles[self.style]

    def image_to_pixels(self, image):
        """Convert image to pixel data with enhanced gradient effect"""
        try:
            logger.info(f"Processing image with style: {self.style}")
            
            # Convert to grayscale and numpy array
            image = image.convert('L')
            
            # Calculate size maintaining aspect ratio
            original_ratio = image.width / image.height
            target_height = self.height
            target_width = int(target_height * original_ratio)
            
            if target_width > self.width:
                target_width = self.width
                target_height = int(target_width / original_ratio)
            
            image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            img_array = np.array(image)
            
            # Create empty pixel array
            pixels = np.zeros((self.height, self.width), dtype=float)
            
            # Calculate centering offsets
            x_offset = (self.width - target_width) // 2
            y_offset = (self.height - target_height) // 2
            
            # Process image based on style
            if self.style == 'simple':
                # Binary threshold (just black and white)
                threshold = 128
                processed = (img_array < threshold).astype(int) * 4
                
            elif self.style == 'gradient':
                # 1. 이미지 반전 (텍스트/이미지가 밝은 값을 가지도록)
                img_array = 255 - img_array
                
                # 2. 정규화 (0-1 범위로)
                img_array = img_array / 255.0
                
                # 3. 가우시안 블러로 부드러운 그라데이션 생성
                blurred = gaussian_filter(img_array, sigma=0.7)  # sigma 값 증가
                
                # 4. 주변부 효과 강화
                y, x = np.ogrid[:target_height, :target_width]
                center_y, center_x = target_height/2, target_width/2
                dist_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                edge_weight = np.power(1 - (dist_from_center / np.max(dist_from_center)), 0.5)  # 거듭제곱으로 효과 강화
                
                # 5. 이미지와 주변부 효과 결합
                combined = blurred * edge_weight
                
                # 6. 5단계 양자화 - 임계값 조정
                processed = np.zeros_like(combined, dtype=int)
                processed[combined > 0.85] = 4    # 가장 진한 색 (빨간색)
                processed[(combined > 0.65) & (combined <= 0.85)] = 3  # 진한 색 (주황색)
                processed[(combined > 0.45) & (combined <= 0.65)] = 2  # 중간 색 (노란색)
                processed[(combined > 0.25) & (combined <= 0.45)] = 1  # 연한 색 (녹색)
                processed[combined <= 0.25] = 0   # 배경 (흰색)
                
            elif self.style == 'border':
                # Edge detection for border effect
                from scipy import ndimage
                processed = np.zeros_like(img_array)
                # Basic threshold first
                binary = (img_array < 128).astype(int)
                # Detect edges
                edges = ndimage.sobel(binary)
                # Combine: edges are darkest, interior is medium
                processed[binary > 0] = 2  # Interior
                processed[np.abs(edges) > 0] = 4  # Edges
                
            else:
                raise ValueError(f"Unknown style: {self.style}")
            
            # Place the processed image in the center
            pixels[
                y_offset:y_offset+target_height,
                x_offset:x_offset+target_width
            ] = processed
            
            logger.info(f"Final pixel array shape: {pixels.shape}")
            return pixels.astype(int)
            
        except Exception as e:
            logger.error(f"Error in image_to_pixels: {str(e)}")
            logger.debug(f"Detailed error:\n{traceback.format_exc()}")
            raise