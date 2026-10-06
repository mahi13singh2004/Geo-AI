import pytest
from shapely.geometry import Polygon, LineString, Point
from app.measurements.polygon import PolygonMeasurement
from app.measurements.linestring import LineStringMeasurement
from app.measurements.registry import MeasurementRegistry


def test_polygon_measurement():
    polygon = Polygon([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)])
    strategy = PolygonMeasurement()
    value, unit, status = strategy.calculate(polygon)
    assert value == 10000.0
    assert unit == "m²"
    assert status == "COMPLETED"


def test_linestring_measurement():
    linestring = LineString([(0, 0), (0, 100)])
    strategy = LineStringMeasurement()
    value, unit, status = strategy.calculate(linestring)
    assert value == 100.0
    assert unit == "m"
    assert status == "COMPLETED"


def test_registry_polygon_supported():
    assert MeasurementRegistry.is_supported("Polygon") == True


def test_registry_point_not_supported():
    assert MeasurementRegistry.is_supported("Point") == False


def test_registry_get_strategy():
    strategy = MeasurementRegistry.get_strategy("Polygon")
    assert strategy is not None
    assert isinstance(strategy, PolygonMeasurement)
