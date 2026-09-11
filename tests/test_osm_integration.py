import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.services.osm_service import get_district_bbox, create_circular_polygon, OsmService
from app.api.v1.endpoints.osm_search import resolve_parent_district

client = TestClient(app)

def test_get_district_bbox():
    # Kallakurichi district bounding box check
    bbox = get_district_bbox("Kallakurichi")
    assert bbox is not None
    min_lat, min_lon, max_lat, max_lon = bbox
    assert min_lat < max_lat
    assert min_lon < max_lon
    # Coordinates for Kallakurichi should encompass center lat=11.7380, lon=78.9620
    assert min_lat <= 11.7380 <= max_lat
    assert min_lon <= 78.9620 <= max_lon

def test_create_circular_polygon():
    lat, lon = 13.0827, 80.2707
    radius = 1.0 # 1 km
    poly = create_circular_polygon(lat, lon, radius)
    
    assert poly["type"] == "Polygon"
    assert len(poly["coordinates"]) == 1
    coords = poly["coordinates"][0]
    assert len(coords) == 17 # 16 vertices + 1 closing vertex
    # Start and end coordinates must match exactly (closed loop)
    assert coords[0] == coords[-1]

def test_resolve_parent_district():
    # Chennai center should resolve to Chennai district
    chennai_lat, chennai_lon = 13.0827, 80.2707
    parent = resolve_parent_district(chennai_lat, chennai_lon, "Chennai Central Railway Station, Tamil Nadu")
    assert parent == "Chennai"
    
    # Kallakurichi center
    parent_k = resolve_parent_district(11.7380, 78.9620, "Kallakurichi Bus Stand, India")
    assert parent_k == "Kallakurichi"

@patch("app.services.osm_service.query_overpass")
def test_osm_service_get_district_features(mock_query):
    # Mock Overpass response
    mock_query.return_value = {
        "elements": [
            {
                "type": "node",
                "id": 123456,
                "lat": 11.7380,
                "lon": 78.9620,
                "tags": {
                    "name": "Ulundurpet",
                    "place": "town",
                    "population": "25000"
                }
            }
        ]
    }
    
    # Clear any cache file if it exists to force query
    cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "raw", "osm_cache", "kallakurichi_places.geojson"))
    if os.path.exists(cache_path):
        try:
            os.remove(cache_path)
        except Exception:
            pass
            
    res = OsmService.get_district_features("Kallakurichi", "places")
    assert res["type"] == "FeatureCollection"
    assert len(res["features"]) > 0
    
    feat = res["features"][0]
    assert feat["properties"]["name"] == "Ulundurpet"
    assert feat["properties"]["district"] == "Kallakurichi"
    assert feat["geometry"]["type"] == "Polygon" # Approximated boundary circle

@patch("urllib.request.urlopen")
def test_osm_search_endpoint(mock_urlopen):
    # Mock Nominatim API response
    mock_response = MagicMock()
    mock_response.read.return_value = b"""
    [
        {
            "osm_id": 98765,
            "lat": "11.6643",
            "lon": "78.1460",
            "display_name": "Attur, Salem, Tamil Nadu, India",
            "type": "town"
        }
    ]
    """
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response
    
    response = client.get("/api/v1/search?q=Attur")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["label"] == "Attur (Salem)"
    assert data[0]["feature"]["properties"]["district"] == "Salem"
