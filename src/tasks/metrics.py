from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import asyncio
from logs.logger import logger


class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def log_timestamp_job(self):
        timestamp = datetime.now().isoformat()
        logger.info(f"Job executed at {timestamp}")
        await asyncio.sleep(0)

    def start(self):
        self.scheduler.add_job(
            func=self.log_timestamp_job,
            trigger=IntervalTrigger(hours=6),
            id="timestamp_logger",
            max_instances=1,
            coalesce=True,
            replace_existing=True,
        )
        self.scheduler.start()
        timestamp = datetime.now().isoformat()
        logger.info(f"Scheduler started {timestamp}")

    def shutdown(self):
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

    def get_status(self):
        job = self.scheduler.get_job("timestamp_logger")
        return {
            "scheduler_running": self.scheduler.running,
            "next_run": job.next_run_time.isoformat() if job else None,
        }
