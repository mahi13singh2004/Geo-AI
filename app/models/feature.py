from typing import Optional, Dict, Any


class FeatureModel:
    def __init__(
        self,
        id: Optional[int],
        file_id: str,
        feature_index: int,
        geometry_type: str,
        geometry: str,
        properties: Optional[Dict[str, Any]],
        source_crs: Optional[str],
        measurement_crs: Optional[str],
        measurement_type: Optional[str],
        measurement_value: Optional[float],
        measurement_unit: Optional[str],
        measurement_status: str,
    ):
        self.id = id
        self.file_id = file_id
        self.feature_index = feature_index
        self.geometry_type = geometry_type
        self.geometry = geometry
        self.properties = properties
        self.source_crs = source_crs
        self.measurement_crs = measurement_crs
        self.measurement_type = measurement_type
        self.measurement_value = measurement_value
        self.measurement_unit = measurement_unit
        self.measurement_status = measurement_status
