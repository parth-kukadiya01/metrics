from typing import Optional
from fastapi import Query, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from pydantic import BaseModel, model_validator
from logics.logic import get_age, get_device_type, get_region, get_gender, get_placement, get_platform
from datetime import datetime

class MetricsValidation(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    region_id: Optional[int] = Query(None, description="Region ID")
    platform_id: Optional[int] = Query(None, description="Platform ID")
    placement_id: Optional[int] = Query(None, ge=0, description="Placement ID")
    device_type_id: Optional[int] = Query(None, ge=0, description="Device Type ID")
    age_id: Optional[int] = Query(None, ge=0, description="Age ID")
    gender_id: Optional[int] = Query(None, ge=0, description="Gender ID")
    min_impressions: Optional[int] = Query(None, ge=0, description="Min Impressions")
    max_cost: Optional[float] = Query(None, gt=0, description="Maximum cost")
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
    offset: int = Query(0, ge=0, description="Number of records to skip")

    def validate_fields(self, db: Session):
        try:
            start_date_obj = datetime.strptime(self.start_date, "%Y-%m-%d").date() if self.start_date else None
            end_date_obj = datetime.strptime(self.end_date, "%Y-%m-%d").date() if self.end_date else None
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        if start_date_obj and end_date_obj and start_date_obj > end_date_obj:
            raise HTTPException(status_code=400, detail="Start date must be before end date.")

        # Validate Foreign Key references
        print("self.gender_id ::", self.gender_id)
        if self.region_id is not None:
            get_region(self.region_id, db)
        if self.platform_id is not None:
            get_platform(self.platform_id, db)
        if self.placement_id is not None:
            get_placement(self.placement_id, db)
        if self.device_type_id is not None:
            get_device_type(self.device_type_id, db)
        if self.age_id is not None:
            get_age(self.age_id, db)
        if self.gender_id is not None:
            get_gender(self.gender_id, db)



class AdMetricsResponse(BaseModel):
    date: Optional[str]
    region: Optional[str]
    age_range: Optional[str]
    gender: Optional[str]
    platform: Optional[str]
    placement: Optional[str]
    device_type: Optional[str]
    impressions: int
    clicks: int
    cost: float
    conversions: int
    likes: int

    class Config:
        orm_mode = True
