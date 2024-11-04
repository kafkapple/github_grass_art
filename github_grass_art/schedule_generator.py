# schedule_generator.py

import numpy as np
from datetime import datetime, timedelta

class ScheduleGenerator:
    def __init__(self, pixel_data):
        self.pixel_data = pixel_data
        self.start_date = self.get_start_date()

    def get_start_date(self):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday() + 1)
        start_date = start_of_week - timedelta(weeks=51)
        return start_date

    def generate_schedule(self):
        """Generate commit schedule based on pixel intensity"""
        schedule = []
        
        for week in range(self.pixel_data.shape[1]):
            for day in range(self.pixel_data.shape[0]):
                intensity = self.pixel_data[day, week]
                if intensity > 0:
                    # Convert intensity levels (1-4) to number of commits
                    num_commits = {
                        1: 2,    # Light green: 2 commits
                        2: 5,    # Medium green: 5 commits
                        3: 8,    # Dark green: 8 commits
                        4: 12,   # Darkest green: 12 commits
                    }[intensity]
                    
                    schedule.extend([self.get_date(week, day)] * num_commits)
        
        return schedule