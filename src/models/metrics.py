from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class DimDate(Base):
    __tablename__ = "dim_date"
    date_id = Column(Integer, primary_key=True)
    date_value = Column(String, nullable=False)

    metrics = relationship("FactAdMetricsDaily", back_populates="date")


class DimRegion(Base):
    __tablename__ = "dim_region"
    region_id = Column(Integer, primary_key=True)
    region_name = Column(String(100), nullable=False)
    metrics = relationship("FactAdMetricsDaily", back_populates="region")


class DimAgeGroup(Base):
    __tablename__ = "dim_age_group"
    age_id = Column(Integer, primary_key=True)
    age_range = Column(String(20), nullable=False)
    metrics = relationship("FactAdMetricsDaily", back_populates="age_group")


class DimGender(Base):
    __tablename__ = "dim_gender"
    gender_id = Column(Integer, primary_key=True)
    gender_name = Column(String(20), nullable=False)
    metrics = relationship("FactAdMetricsDaily", back_populates="gender")


class DimPlatform(Base):
    __tablename__ = "dim_platform"
    platform_id = Column(Integer, primary_key=True)
    platform_name = Column(String(50), nullable=False)
    metrics = relationship("FactAdMetricsDaily", back_populates="platform")


class DimPlacement(Base):
    __tablename__ = "dim_placement"
    placement_id = Column(Integer, primary_key=True)
    placement_name = Column(String(100), nullable=False)
    metrics = relationship("FactAdMetricsDaily", back_populates="placement")


class DimDeviceType(Base):
    __tablename__ = "dim_device_type"
    device_type_id = Column(Integer, primary_key=True)
    device_type_name = Column(String(50), nullable=False)
    metrics = relationship("FactAdMetricsDaily", back_populates="device_type")


class FactAdMetricsDaily(Base):
    __tablename__ = "fact_ad_metrics_daily"
    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"))
    region_id = Column(Integer, ForeignKey("dim_region.region_id"))
    age_id = Column(Integer, ForeignKey("dim_age_group.age_id"))
    gender_id = Column(Integer, ForeignKey("dim_gender.gender_id"))
    platform_id = Column(Integer, ForeignKey("dim_platform.platform_id"))
    placement_id = Column(Integer, ForeignKey("dim_placement.placement_id"))
    device_type_id = Column(Integer, ForeignKey("dim_device_type.device_type_id"))
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    conversions = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)

    date = relationship("DimDate", back_populates="metrics")
    region = relationship("DimRegion", back_populates="metrics")
    age_group = relationship("DimAgeGroup", back_populates="metrics")
    gender = relationship("DimGender", back_populates="metrics")
    platform = relationship("DimPlatform", back_populates="metrics")
    placement = relationship("DimPlacement", back_populates="metrics")
    device_type = relationship("DimDeviceType", back_populates="metrics")
