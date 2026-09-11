import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.population_service import PopulationService

client = TestClient(app)

def test_population_service_abstract():
    # 1. Verify Nilgiris Census Excel Abstract parsing
    df = PopulationService.get_census_data("The Nilgiris")
    assert df is not None
    assert len(df) == 57
    
    cols = list(df.columns)
    assert "Level" in cols
    assert "Name" in cols
    assert "CD Block_Code" in cols
    assert "Total Population Person" in cols
    assert "Total Population Male" in cols
    assert "Total Population Female" in cols
    assert "No of Households" in cols

def test_theni_population_service_abstract():
    # 2. Verify Theni Census Excel Abstract parsing from data1
    df = PopulationService.get_census_data("Theni")
    assert df is not None
    assert len(df) == 125
    assert df["District_Code"].iloc[0] == 624
    assert df["State/UTs_Code"].iloc[0] == 33
    
    # 98 villages and 27 CD block records
    level_counts = df["Level"].value_counts().to_dict()
    assert level_counts["VILLAGE"] == 98
    assert level_counts["CD BLOCK"] == 27
    
    # Check Ward_Code is 0 for all rows (no fake ward conversions)
    assert (df["Ward_Code"] == 0).all()

def test_theni_hierarchy_resolution():
    hierarchy = PopulationService.get_theni_hierarchy()
    assert len(hierarchy) == 9
    assert "Andipatti" in hierarchy
    assert "Periyakulam" in hierarchy
    assert "Theni" in hierarchy
    assert "Bodinayakanur" in hierarchy
    
    # Check village attributes in Andipatti
    andipatti_villages = hierarchy["Andipatti"]
    assert len(andipatti_villages) == 18
    first_v = andipatti_villages[0]
    assert isinstance(first_v["population"], int)
    assert first_v["population"] > 0
    assert first_v["geographic_level"] == "Village"
    assert first_v["boundary_status"] == "Population boundary unavailable"
    assert first_v["join_status"] == "NO_BOUNDARY_POLYGON"

def test_theni_population_geojson():
    geojson = PopulationService.get_theni_population_geojson()
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == 1
    
    feature = geojson["features"][0]
    assert feature["geometry"]["type"] in ["Polygon", "MultiPolygon"]
    props = feature["properties"]
    assert props["name"] == "Theni District"
    assert props["district"] == "Theni"
    assert props["population"] == 575418
    assert props["boundary_status"] == "Verified Administrative Boundary"
    assert props["join_status"] == "MATCHED (District Administrative Polygon)"
    assert props["sub_district_boundaries_available"] is False

def test_population_endpoints():
    # 1. GeoJSON endpoint test for The Nilgiris
    response = client.get("/api/v1/population/geojson?district=The+Nilgiris")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0
    for f in data["features"]:
        assert f["geometry"]["type"] in ["Polygon", "MultiPolygon"]
    
    # 2. GeoJSON endpoint test for Theni
    res_theni = client.get("/api/v1/population/geojson?district=Theni")
    assert res_theni.status_code == 200
    t_data = res_theni.json()
    assert t_data["type"] == "FeatureCollection"
    assert len(t_data["features"]) == 1
    assert t_data["features"][0]["geometry"]["type"] in ["Polygon", "MultiPolygon"]
    assert t_data["features"][0]["properties"]["population"] == 575418

    # 3. Population zones endpoint test for Theni
    res_theni_zones = client.get("/api/v1/population-zones/geojson?district=Theni")
    assert res_theni_zones.status_code == 200
    tz_data = res_theni_zones.json()
    assert len(tz_data["features"]) == 1

    # 4. Benchmark Population Choropleth endpoint for Chennai
    res_chennai = client.get("/api/v1/population-zones/geojson?district=Chennai")
    assert res_chennai.status_code == 200
    c_data = res_chennai.json()
    assert c_data["type"] == "FeatureCollection"
    assert len(c_data["features"]) > 0

    # 5. Hierarchy API endpoint test for Theni
    res_hier = client.get("/api/v1/population/theni/hierarchy")
    assert res_hier.status_code == 200
    h_data = res_hier.json()
    assert "Andipatti" in h_data
    assert len(h_data["Andipatti"]) > 0
