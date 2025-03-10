from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.logics.metrics import fetch_ad_metrics
from src.logs.logger import logger
from src.schemas.metrics import MetricsValidation

router = APIRouter()

@router.get("/")
async def get_ad_metrics(query_params:MetricsValidation = Depends(),
    db: Session = Depends(get_db)):

    try:
        query_params.validate_fields(db)
        results = fetch_ad_metrics(
            db=db,
            start_date=query_params.start_date,
            end_date=query_params.end_date,
            region_id=query_params.region_id,
            platform_id=query_params.platform_id,
            min_impressions=query_params.min_impressions,
            max_cost=query_params.max_cost,
            limit=query_params.limit,
            offset=query_params.offset
        )
        logger.info(f"Fetched {len(results)} ad metrics records")

        return results
    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")