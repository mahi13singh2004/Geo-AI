from pydantic import BaseModel
from typing import List, Optional


class MeasurementDetail(BaseModel):
    type: str
    value: float
    unit: str


class FeatureMeasurement(BaseModel):
    feature_id: int
    geometry_type: str
    measurement: Optional[MeasurementDetail]
    measurement_status: str


class MeasurementsResponse(BaseModel):
    file_id: str
    page: int
    limit: int
    total: int
    results: List[FeatureMeasurement]
