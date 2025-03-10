from sqlalchemy.orm import Session
from src.models.metrics import *
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from src.schemas.metrics import AdMetricsResponse
import traceback

def get_date_id(db: Session, date_value: datetime.date) -> int:
    date_str = date_value.strftime('%Y-%m-%d')
    date_record = db.query(DimDate).filter(DimDate.date_value == date_str).first()
    if not date_record:
        return 0
    return date_record.date_id


def fetch_ad_metrics(
    db: Session,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    region_id: Optional[int] = None,
    platform_id: Optional[int] = None,
    placement_id: Optional[int] = None,
    device_type_id: Optional[int] = None,
    age_id: Optional[int] = None,
    gender_id: Optional[int] = None,
    min_impressions: Optional[int] = None,
    max_cost: Optional[float] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:

    try:
        query = db.query(FactAdMetricsDaily)

        if start_date:
            try:
                start_date_id = get_date_id(db, start_date)
                query = query.filter(FactAdMetricsDaily.date_id >= start_date_id)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid start date format: '{start_date}'. Please use YYYY-MM-DD (e.g., 2025-03-07)."
                )

        if end_date:
            try:
                end_date_id = get_date_id(db, end_date)
                query = query.filter(FactAdMetricsDaily.date_id <= end_date_id)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid end date format: '{end_date}'. Please use YYYY-MM-DD (e.g., 2025-03-07)."
                )

        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date range: Start date ({start_date}) must be before end date ({end_date})."
            )

        if region_id is not None:
            query = query.filter(FactAdMetricsDaily.region_id == region_id)
        if age_id is not None:
            query = query.filter(FactAdMetricsDaily.age_id == age_id)
        if placement_id is not None:
            query = query.filter(FactAdMetricsDaily.placement_id == placement_id)
        if device_type_id is not None:
            query = query.filter(FactAdMetricsDaily.device_type_id == device_type_id)
        if gender_id is not None:
            query = query.filter(FactAdMetricsDaily.gender_id == gender_id)
        if platform_id is not None:
            query = query.filter(FactAdMetricsDaily.platform_id == platform_id)
        if min_impressions is not None:
            query = query.filter(FactAdMetricsDaily.impressions >= min_impressions)
        if max_cost is not None:
            query = query.filter(FactAdMetricsDaily.cost <= max_cost)

        if limit <= 0 or offset < 0:
            raise HTTPException(
                status_code=400,
                detail="Limit must be positive and offset cannot be negative."
            )

        results = query.offset(offset).limit(limit).all()

        if not results:
            return {"data": [], "total_records":0}

        data = [
            AdMetricsResponse(
                date=result.date.date_value,
                region=result.region.region_name if result.region else None,
                age_range=result.age_group.age_range if result.age_group else None,
                gender=result.gender.gender_name if result.gender else None,
                platform=result.platform.platform_name if result.platform else None,
                placement=result.placement.placement_name if result.placement else None,
                device_type=result.device_type.device_type_name if result.device_type else None,
                impressions=result.impressions,
                clicks=result.clicks,
                cost=result.cost,
                conversions=result.conversions,
                likes=result.likes,
            )
            for result in results
        ]

        return {
            "data": data,
            "total_records": len(data)
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        stack_trace = traceback.format_exc()
        error_detail = (
            f"An unexpected error occurred while processing your request: {str(e)}.\n"
            f"Details for debugging:\n{stack_trace}"
        )
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )