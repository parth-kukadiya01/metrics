from typing import Optional
from fastapi import Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from src.logics.logic import (
    get_age,
    get_device_type,
    get_region,
    get_gender,
    get_placement,
    get_platform,
)
from datetime import datetime


class MetricsValidation(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    region_id: Optional[int] = None
    platform_id: Optional[int] = None
    placement_id: Optional[int] = None
    device_type_id: Optional[int] = None
    age_id: Optional[int] = None
    gender_id: Optional[int] = None
    min_impressions: Optional[int] = None
    max_cost: Optional[float] = None
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
    offset: int = Query(0, ge=0, description="Number of records to skip")

    @field_validator("region_id", "platform_id", "placement_id", "device_type_id", "age_id", "gender_id", "min_impressions", "max_cost",  mode="before")
    @classmethod
    def validate_positive_integer(cls, value, field):
        if value is not None :
            try:
                if field.field_name == "max_cost":
                    if not isinstance(value, float) or float(value) <= 0:
                        raise ValueError
                if not isinstance(value, int) or value <= 0:
                    raise ValueError
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={"error": f"Invalid value for {field.field_name}. Expected a positive integer/float."}
                )
        return value

    @field_validator("start_date", "end_date", mode="after")
    @classmethod
    def validate_date_format(cls, value, field):
        if value:
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={"error": f"Invalid date format for {field.field_name}. Use YYYY-MM-DD."},
                )
        return value

    def validate_fields(self, db: Session):
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
        from_attributes = True  # Pydantic v2 replacement for `orm_mode`
