from shapely.geometry import LineString
from app.measurements.base import MeasurementStrategy
from typing import Optional, Tuple


class LineStringMeasurement(MeasurementStrategy):
    def calculate(
        self, geometry: LineString
    ) -> Tuple[Optional[float], Optional[str], str]:
        try:
            length = geometry.length
            return length, "m", "COMPLETED"
        except Exception:
            return None, None, "CALCULATION_FAILED"
