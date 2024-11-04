# schedule_generator.py

import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ScheduleGenerator:
    def __init__(self, pixel_data):
        self.pixel_data = pixel_data
        # 현재 날짜로부터 52주 전으로 시작
        self.start_date = datetime.now() - timedelta(weeks=52)
        logger.info(f"Initialized ScheduleGenerator with start date: {self.start_date}")

    def get_date(self, week, day):
        """Calculate date for given week and day"""
        try:
            # week: 0-51 (52주), day: 0-6 (일-토)
            target_date = self.start_date + timedelta(weeks=week, days=day)
            logger.debug(f"Generated date for week {week}, day {day}: {target_date}")
            return target_date
        except Exception as e:
            logger.error(f"Error generating date for week {week}, day {day}: {str(e)}")
            raise

    def generate_schedule(self):
        """Generate commit schedule based on pixel intensity"""
        try:
            schedule = []
            logger.info("Generating commit schedule...")
            
            for week in range(self.pixel_data.shape[1]):  # 52주
                for day in range(self.pixel_data.shape[0]):  # 7일
                    intensity = self.pixel_data[day, week]
                    if intensity > 0:
                        # Convert intensity levels (1-4) to number of commits
                        num_commits = {
                            1: 2,    # Light green: 2 commits
                            2: 5,    # Medium green: 5 commits
                            3: 8,    # Dark green: 8 commits
                            4: 12,   # Darkest green: 12 commits
                        }.get(intensity, 0)
                        
                        date = self.get_date(week, day)
                        schedule.extend([date] * num_commits)
            
            logger.info(f"Generated schedule with {len(schedule)} commits")
            return schedule
            
        except Exception as e:
            logger.error(f"Error generating schedule: {str(e)}")
            raise