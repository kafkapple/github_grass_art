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
        schedule = []
        height, width = self.pixel_data.shape
        for x in range(width):
            for y in range(height):
                if self.pixel_data[y, x]:
                    commit_date = self.start_date + timedelta(weeks=x, days=y)
                    schedule.append(commit_date)
        schedule.sort()
        return schedule