from sqlalchemy.orm import Session
from models.metrics import *
from fastapi import HTTPException


def get_region(region_id: int, db: Session):
    region = db.query(DimRegion).filter(DimRegion.region_id == region_id).first()
    if not region:
        raise HTTPException(
            status_code=400, detail=f"Region with ID {region_id} not found"
        )
    return region


def get_platform(platform_id: int, db: Session):
    platform = (
        db.query(DimPlatform).filter(DimPlatform.platform_id == platform_id).first()
    )
    if not platform:
        raise HTTPException(
            status_code=400, detail=f"Platform with ID {platform_id} not found"
        )
    return platform


def get_placement(placement_id: int, db: Session):
    placement = (
        db.query(DimPlacement).filter(DimPlacement.placement_id == placement_id).first()
    )
    if not placement:
        raise HTTPException(
            status_code=400, detail=f"Placement with ID {placement_id} not found"
        )
    return placement


def get_device_type(device_type_id: int, db: Session):
    device_type = (
        db.query(DimDeviceType)
        .filter(DimDeviceType.device_type_id == device_type_id)
        .first()
    )
    if not device_type:
        raise HTTPException(
            status_code=400, detail=f"Device Type with ID {device_type_id} not found"
        )
    return device_type


def get_age(age_id: int, db: Session):
    age = db.query(DimAgeGroup).filter(DimAgeGroup.age_id == age_id).first()
    if not age:
        raise HTTPException(
            status_code=400, detail=f"Age Group with ID {age_id} not found"
        )
    return age


def get_gender(gender_id: int, db: Session):
    gender = db.query(DimGender).filter(DimGender.gender_id == gender_id).first()
    if not gender:
        raise HTTPException(
            status_code=400, detail=f"Gender with ID {gender_id} not found"
        )
    return gender
