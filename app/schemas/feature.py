from pydantic import BaseModel
from typing import Optional, Dict, Any


class FeatureResponse(BaseModel):
    feature_id: int
    geometry_type: str
    measurement: Optional[Dict[str, Any]]
    measurement_status: str
