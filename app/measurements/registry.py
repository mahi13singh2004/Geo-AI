from app.measurements.polygon import PolygonMeasurement
from app.measurements.linestring import LineStringMeasurement
from app.measurements.base import MeasurementStrategy
from typing import Optional


class MeasurementRegistry:
    _strategies = {
        "Polygon": PolygonMeasurement(),
        "MultiPolygon": PolygonMeasurement(),
        "LineString": LineStringMeasurement(),
        "MultiLineString": LineStringMeasurement(),
    }

    @classmethod
    def get_strategy(cls, geometry_type: str) -> Optional[MeasurementStrategy]:
        return cls._strategies.get(geometry_type)

    @classmethod
    def is_supported(cls, geometry_type: str) -> bool:
        return geometry_type in cls._strategies
