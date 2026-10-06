from pyproj import CRS, Transformer
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform
from typing import Optional, Tuple
import math
import logging

logger = logging.getLogger(__name__)


class CRSService:
    @staticmethod
    def is_geographic(crs_string: Optional[str]) -> bool:
        if not crs_string:
            return False
        try:
            crs = CRS.from_string(crs_string)
            return crs.is_geographic
        except Exception:
            return False

    @staticmethod
    def determine_utm_zone(lon: float, lat: float) -> str:
        zone = int((lon + 180) / 6) + 1
        hemisphere = "north" if lat >= 0 else "south"
        return f"EPSG:{32600 + zone if hemisphere == 'north' else 32700 + zone}"
