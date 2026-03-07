#!/usr/bin/env python3
"""
AutoPilot - Task Scheduler
"""

from apscheduler.schedulers.background import BackgroundScheduler
import logging

class AutoPilot:
    def __init__(self, config, controller):
        self.config = config
        self.controller = controller
        self.scheduler = BackgroundScheduler()
        self.logger = logging.getLogger('AutoPilot')

    def start(self):
        if self.config['automation']['scheduler_enabled']:
            self.scheduler.start()
            self.logger.info("AutoPilot Scheduler started.")

    def add_job(self, func, trigger, **kwargs):
        self.scheduler.add_job(func, trigger, **kwargs)
