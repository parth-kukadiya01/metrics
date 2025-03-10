
from src.core.app import app
from . import metrics

app.include_router(metrics.router, prefix="/ad-metrics", tags=["metrics"])


