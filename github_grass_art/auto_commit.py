# auto_commit.py

import os
import subprocess
from datetime import datetime
from github_grass_art.schedule_generator import ScheduleGenerator

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
        print("All commits completed.")

    def push(self):
        subprocess.call(['git', 'push', 'origin', 'main'])
        print("Pushed to remote repository.")
