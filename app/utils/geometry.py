from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry


def validate_geometry(geom: BaseGeometry) -> bool:
    if geom is None or geom.is_empty:
        return False
    return geom.is_valid


def get_geometry_type(geom: BaseGeometry) -> str:
    return geom.geom_type
