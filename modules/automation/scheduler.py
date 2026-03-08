"""
Automation Scheduler for v5.0
Uses APScheduler for time-based tasks
"""

from apscheduler.schedulers.background import BackgroundScheduler
import datetime

class AutomationScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def add_job(self, func, trigger, **kwargs):
        """
        trigger can be 'interval', 'cron', or 'date'
        """
        return self.scheduler.add_job(func, trigger, **kwargs)

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def list_jobs(self):
        return self.scheduler.get_jobs()

    def shutdown(self):
        self.scheduler.shutdown()
