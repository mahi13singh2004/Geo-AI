from shapely.geometry import Polygon
from app.measurements.base import MeasurementStrategy
from typing import Optional, Tuple


class PolygonMeasurement(MeasurementStrategy):
    def calculate(self, geometry: Polygon) -> Tuple[Optional[float], Optional[str], str]:
        try:
            area = geometry.area
            return area, "m²", "COMPLETED"
        except Exception:
            return None, None, "CALCULATION_FAILED"
