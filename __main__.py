# __main__.py

from image_processor import ImageProcessor
from preview_generator import PreviewGenerator
from schedule_generator import ScheduleGenerator
from auto_commit import AutoCommitter

def main():
    # 1. 이미지 처리
    input_data = input("원하는 글자 또는 이미지 파일 경로를 입력하세요: ")
    is_text = True  # 텍스트인지 이미지인지 판단 로직 추가 가능
    processor = ImageProcessor(input_data, is_text=is_text)
    pixel_data = processor.process()

    # 2. 미리보기 생성
    preview = PreviewGenerator(pixel_data)
    preview.generate_preview()

    # 3. 커밋 스케줄 생성
    scheduler = ScheduleGenerator(pixel_data)
    schedule = scheduler.generate_schedule()

    # 4. 자동 커밋 실행
    repo_path = input("로컬 리포지토리 경로를 입력하세요: ")
    committer = AutoCommitter(schedule, repo_path)
    committer.commit()
    committer.push()

if __name__ == "__main__":
    main()