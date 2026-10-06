import pytest
from app.services.crs_service import CRSService


def test_is_geographic_epsg_4326():
    assert CRSService.is_geographic("EPSG:4326") == True


def test_is_geographic_utm():
    assert CRSService.is_geographic("EPSG:32633") == False


def test_is_geographic_none():
    assert CRSService.is_geographic(None) == False


def test_determine_utm_zone_northern():
    zone = CRSService.determine_utm_zone(10.0, 50.0)
    assert zone == "EPSG:32632"


def test_determine_utm_zone_southern():
    zone = CRSService.determine_utm_zone(10.0, -50.0)
    assert zone == "EPSG:32732"


def test_determine_utm_zone_equator():
    zone = CRSService.determine_utm_zone(0.0, 0.0)
    assert "EPSG:326" in zone
