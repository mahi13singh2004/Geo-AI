import pytest
from shapely.geometry import Polygon, Point
from app.utils.geometry import validate_geometry, get_geometry_type


def test_validate_valid_geometry():
    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    assert validate_geometry(polygon) == True


def test_validate_empty_geometry():
    polygon = Polygon()
    assert validate_geometry(polygon) == False


def test_validate_none_geometry():
    assert validate_geometry(None) == False


def test_get_geometry_type():
    point = Point(0, 0)
    assert get_geometry_type(point) == "Point"
    
    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    assert get_geometry_type(polygon) == "Polygon"
