# auto_commit.py

import os
import subprocess
from datetime import datetime
from schedule_generator import ScheduleGenerator

class AutoCommitter:
    def __init__(self, schedule, repo_path):
        self.schedule = schedule
        self.repo_path = repo_path

    def commit(self):
        os.chdir(self.repo_path)
        for commit_date in self.schedule:
            date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S')
            with open('commit.txt', 'a') as f:
                f.write(f"Commit on {date_str}\n")
            subprocess.call(['git', 'add', 'commit.txt'])
            env = os.environ.copy()
            env['GIT_AUTHOR_DATE'] = date_str
            env['GIT_COMMITTER_DATE'] = date_str
            subprocess.call(['git', 'commit', '-m', f'Auto commit on {date_str}'], env=env)
        print("모든 커밋이 완료되었습니다.")

    def push(self):
        subprocess.call(['git', 'push', 'origin', 'main'])
        print("원격 저장소로 푸시되었습니다.")