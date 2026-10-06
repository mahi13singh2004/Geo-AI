from shapely.geometry.base import BaseGeometry
from app.measurements.registry import MeasurementRegistry
from app.services.crs_service import CRSService
from app.models.measurement import Measurement
from pyproj import Transformer
from shapely.ops import transform
import logging

logger = logging.getLogger(__name__)


class MeasurementService:
    def __init__(self):
        self.crs_service = CRSService()

    def calculate_measurement(
        self, geometry: BaseGeometry, crs: str, geometry_type: str
    ) -> Measurement:
        if geometry_type == "Point":
            return Measurement(None, None, None, "NOT_REQUIRED")

        if not MeasurementRegistry.is_supported(geometry_type):
            return Measurement(None, None, None, "NOT_SUPPORTED")

        try:
            projected_geom = geometry
            measurement_crs = crs

            if self.crs_service.is_geographic(crs):
                centroid = geometry.centroid
                utm_epsg = self.crs_service.determine_utm_zone(
                    centroid.x, centroid.y
                )
                transformer = Transformer.from_crs(crs, utm_epsg, always_xy=True)
                projected_geom = transform(transformer.transform, geometry)
                measurement_crs = utm_epsg

            strategy = MeasurementRegistry.get_strategy(geometry_type)
            value, unit, status = strategy.calculate(projected_geom)

            if status == "COMPLETED":
                return Measurement(
                    "area" if "Polygon" in geometry_type else "length",
                    value,
                    unit,
                    status,
                )
            return Measurement(None, None, None, status)

        except Exception as e:
            logger.error(f"Measurement calculation failed: {str(e)}")
            return Measurement(None, None, None, "CALCULATION_FAILED")
