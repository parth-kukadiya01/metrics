from fastapi import FastAPI
from logs.logger import logger
from tasks.metrics import SchedulerService

app = FastAPI()

scheduler_service = SchedulerService()

@app.on_event("startup")
async def startup_event():
    scheduler_service.start()
    logger.info("Application started")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler_service.shutdown()
    logger.info("Application shutdown")


