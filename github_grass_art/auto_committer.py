import os
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class AutoCommitter:
    """GitHub 커밋 자동화 클래스"""
    
    def __init__(self, schedule_input, repo_path=None):
        """
        Initialize AutoCommitter
        
        Args:
            schedule_input: 스케줄 파일 경로(str/Path) 또는 스케줄 리스트
            repo_path: Git 저장소 경로 (선택적)
        """
        self.repo_path = Path(repo_path) if repo_path else None
        
        # 스케줄 로드
        if isinstance(schedule_input, (str, Path)):
            self.schedule_file = Path(schedule_input)
            self.load_schedule_from_file()
        else:
            self.schedule = schedule_input
            logger.info(f"Initialized with {len(self.schedule)} scheduled commits")

    def load_schedule_from_file(self):
        """스케줄 파일에서 커밋 일정 로드"""
        try:
            if not self.schedule_file.exists():
                raise FileNotFoundError(f"Schedule file not found: {self.schedule_file}")
                
            with open(self.schedule_file, 'r') as f:
                self.schedule = json.load(f)
            logger.info(f"Loaded {len(self.schedule)} commits from {self.schedule_file}")
        except Exception as e:
            logger.error(f"Error loading schedule: {e}")
            raise

    def should_commit(self, target_date):
        """특정 날짜에 커밋해야 하는지 확인"""
        current_time = datetime.now()
        target_time = datetime.strptime(target_date, '%Y-%m-%d %H:%M:%S')
        return current_time >= target_time

    def make_commit(self, commit_date):
        """지정된 날짜로 커밋 생성"""
        try:
            date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S')
            
            # 커밋 파일 생성/수정
            commit_file = Path(self.repo_path) / 'commit.txt'
            with open(commit_file, 'a') as f:
                f.write(f"Commit on {date_str}\n")
            
            # Git 명령어 실행
            env = os.environ.copy()
            env['GIT_AUTHOR_DATE'] = date_str
            env['GIT_COMMITTER_DATE'] = date_str
            
            subprocess.run(['git', 'add', 'commit.txt'], check=True)
            subprocess.run(
                ['git', 'commit', '-m', f'Auto commit on {date_str}'],
                env=env,
                check=True
            )
            
            logger.info(f"Created commit for {date_str}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Error making commit: {e}")
            raise

    def commit_all(self):
        """모든 예약된 커밋 실행"""
        try:
            if not self.repo_path:
                raise ValueError("Repository path not set")
            
            # 저장소 디렉토리로 이동
            original_dir = os.getcwd()
            os.chdir(self.repo_path)
            
            try:
                for commit_date in self.schedule:
                    self.make_commit(commit_date)
                logger.info("All commits completed successfully")
            finally:
                # 원래 디렉토리로 복귀
                os.chdir(original_dir)
                
        except Exception as e:
            logger.error(f"Error during commit process: {e}")
            raise

    def push(self):
        """변경사항을 원격 저장소에 푸시"""
        try:
            if not self.repo_path:
                raise ValueError("Repository path not set")
                
            os.chdir(self.repo_path)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            logger.info("Successfully pushed to remote repository")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Push failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during push: {e}")
            raise

    def run(self):
        """GitHub Actions에서 사용할 실행 메서드"""
        try:
            current_date = datetime.now()
            commits_to_make = [
                date for date in self.schedule 
                if self.should_commit(date)
            ]
            
            if commits_to_make:
                self.commit_all()
                self.push()
                logger.info(f"Completed {len(commits_to_make)} commits")
            else:
                logger.info("No commits scheduled for current time")
                
        except Exception as e:
            logger.error(f"Run failed: {e}")
            raise