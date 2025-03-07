from sqlalchemy.orm import Session
from models.metrics import *
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from schemas.metrics import AdMetricsResponse


def get_date_id(db: Session, date_value: datetime) -> int:
    date_record = db.query(DimDate).filter(DimDate.date_value == str(date_value)).first()
    if not date_record:
        raise HTTPException(status_code=400, detail=f"No matching date_id found for {date_value}. Ensure the date exists in dim_date.")
    return date_record.date_id


def fetch_ad_metrics(
    db: Session,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    region_id: Optional[int] = None,
    platform_id: Optional[int] = None,
    min_impressions: Optional[int] = None,
    max_cost: Optional[float] = None,
    limit: int = 100,
    offset: int = 0
):
    try:
        query = db.query(FactAdMetricsDaily)
        if start_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            start_date_id = get_date_id(db, start_date_obj)
            query = query.filter(FactAdMetricsDaily.date_id >= start_date_id)
        
        if end_date:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            end_date_id = get_date_id(db, end_date_obj)
            query = query.filter(FactAdMetricsDaily.date_id <= end_date_id)

        if start_date and end_date and start_date_obj > end_date_obj:
            raise HTTPException(status_code=400, detail="Start date must be before end date.")
        
        if region_id is not None:
            query = query.filter(FactAdMetricsDaily.region_id == region_id)
        if platform_id is not None:
            query = query.filter(FactAdMetricsDaily.platform_id == platform_id)
        if min_impressions is not None:
            query = query.filter(FactAdMetricsDaily.impressions >= min_impressions)
        if max_cost is not None:
            query = query.filter(FactAdMetricsDaily.cost <= max_cost)
        
        results = query.offset(offset).limit(limit).all()
        if not results:
            return {"data":[]}
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
            
        return {"data": data}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


