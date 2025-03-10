import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/ad_metrics_db")
    LOG_FILE = "src/logs/app.log"

settings = Settings()
