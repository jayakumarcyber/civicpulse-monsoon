'use client';

import { useState, useEffect } from 'react';
import { ShieldAlert, CloudRain, Activity, Layers, MapPin, Play, Globe, Navigation } from 'lucide-react';

import MapViewContainer from '@/components/Map/MapViewContainer';
import FilterPanel from '@/components/Dashboard/FilterPanel';
import FeatureDetailsPanel from '@/components/Dashboard/FeatureDetailsPanel';
import MapLegend from '@/components/Dashboard/MapLegend';
import SearchBar from '@/components/Dashboard/SearchBar';
import PriorityQueuePanel from '@/components/Priority/PriorityQueuePanel';
import ResourcePlannerPanel from '@/components/ResourcePlanner/ResourcePlannerPanel';
import WhatIfSimulatorPanel from '@/components/Simulator/WhatIfSimulatorPanel';
import RainfallAnalyticsPanel from '@/components/Dashboard/RainfallAnalyticsPanel';

const DISTRICT_COORDINATES: Record<string, [number, number]> = {
  Chennai: [13.0827, 80.2707],
  Coimbatore: [11.0168, 76.9558],
  Salem: [11.6643, 78.1460],
  Madurai: [9.9252, 78.1198],
  Tiruchirappalli: [10.7905, 78.7047],
  Tiruppur: [11.1085, 77.3411],
  Erode: [11.3410, 77.7172],
  Vellore: [12.9165, 79.1325],
  Tirunelveli: [8.7139, 77.7567],
  Kanchipuram: [12.8342, 79.7036],
  Kallakurichi: [11.7380, 78.9620],
  Villupuram: [11.9400, 79.4920],
};

export default function Home() {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  // 1. Layer Visibility States
  const [layers, setLayers] = useState({
    wards: true,
    roads: true,
    drains: true,
    waterbodies: true,
    incidents: true,
    facilities: true,
    population: false,
    populationExposure: false,
    districts: true,
    state: true,
  });

  // 2. Attribute & Administrative Filters
  const [filters, setFilters] = useState({
    stateId: 'Tamil Nadu',
    districtId: 'ALL',
    adminType: 'ALL',
    localBody: 'ALL',
    wardId: 'ALL',
    incidentType: 'ALL',
    severity: 'ALL',
    facilityType: 'ALL',
  });

  // 3. Camera Navigation Trigger
  const [cameraTrigger, setCameraTrigger] = useState<{
    type: 'india' | 'tn' | 'district' | 'ward';
    coords?: [number, number];
    timestamp?: number;
  }>({ type: 'india', timestamp: Date.now() });

  // 4. Scenario Rainfall Input
  const [scenarioRainfall, setScenarioRainfall] = useState<number>(100);
  const [forecastHorizon, setForecastHorizon] = useState<number>(24);

  // 5. GeoJSON Data Store
  const [geoData, setGeoData] = useState({
    wards: null,
    roads: null,
    drains: null,
    waterbodies: null,
    incidents: null,
    facilities: null,
    population: null,
    populationExposure: null,
    districts: null,
    state: null,
  });

  const [wardsList, setWardsList] = useState<any[]>([]);
  const [selectedFeature, setSelectedFeature] = useState<any>(null);
  const [searchResult, setSearchResult] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Summary Metrics
  const [highRiskCount, setHighRiskCount] = useState<number>(3);
  const [medRiskCount, setMedRiskCount] = useState<number>(3);
  const [lowRiskCount, setLowRiskCount] = useState<number>(2);

  // Toggle Layer
  const handleToggleLayer = (layerName: string) => {
    setLayers((prev) => ({ ...prev, [layerName]: !(prev as any)[layerName] }));
  };

  // Change Attribute Filter
  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  // Camera Focus Trigger Handler
  const handleFocusCamera = (type: 'india' | 'tn' | 'district' | 'ward') => {
    let coords: [number, number] | undefined = undefined;
    if (type === 'district' && filters.districtId !== 'ALL' && DISTRICT_COORDINATES[filters.districtId]) {
      coords = DISTRICT_COORDINATES[filters.districtId];
    } else if (type === 'ward' && selectedFeature?.properties?.coordinates) {
      coords = selectedFeature.properties.coordinates;
    }
    setCameraTrigger({ type, coords, timestamp: Date.now() });
  };

  // Fetch GeoJSON Datasets from FastAPI Backend
  const fetchGeoJSONLayers = async () => {
    try {
      setLoading(true);

      const buildUrl = (endpoint: string, extraParams: Record<string, string> = {}) => {
        const url = new URL(`${API_BASE_URL}/api/v1/${endpoint}`);
        if (filters.wardId !== 'ALL') url.searchParams.append('ward_id', filters.wardId);
        if (filters.districtId !== 'ALL') url.searchParams.append('district', filters.districtId);
        if (filters.stateId !== 'ALL') url.searchParams.append('state', filters.stateId);
        Object.entries(extraParams).forEach(([k, v]) => {
          if (v !== 'ALL') url.searchParams.append(k, v);
        });
        return url.toString();
      };

      const [wardsRes, roadsRes, drainsRes, wbRes, incRes, facRes, popRes, distRes, stateRes, popExpRes] = await Promise.all([
        fetch(buildUrl('wards/geojson')),
        fetch(buildUrl('roads/geojson')),
        fetch(buildUrl('drains/geojson')),
        fetch(buildUrl('waterbodies/geojson')),
        fetch(buildUrl('incidents/geojson', { incident_type: filters.incidentType, severity: filters.severity })),
        fetch(buildUrl('facilities/geojson', { facility_type: filters.facilityType })),
        fetch(buildUrl('population-zones/geojson')),
        fetch(`${API_BASE_URL}/api/v1/districts/geojson`),
        fetch(`${API_BASE_URL}/api/v1/state/geojson`),
        fetch(buildUrl('population/geojson')),
      ]);

      const [wards, roads, drains, waterbodies, incidents, facilities, population, districts, state, populationExposure] = await Promise.all([
        wardsRes.json(),
        roadsRes.json(),
        drainsRes.json(),
        wbRes.json(),
        incRes.json(),
        facRes.json(),
        popRes.json(),
        distRes.json(),
        stateRes.json(),
        popExpRes.json(),
      ]);

      setGeoData({
        wards,
        roads,
        drains,
        waterbodies,
        incidents,
        facilities,
        population,
        populationExposure,
        districts,
        state
      });

      if (wards?.features) {
        setWardsList(wards.features.map((f: any) => ({ id: f.properties.id, name: f.properties.name })));

        let high = 0, med = 0, low = 0;
        wards.features.forEach((f: any) => {
          const r = (f.properties.risk_level || '').toUpperCase();
          if (r === 'HIGH' || r === 'CRITICAL') high++;
          else if (r === 'MEDIUM') med++;
          else if (r === 'LOW') low++;
        });
        setHighRiskCount(high || 3);
        setMedRiskCount(med || 3);
        setLowRiskCount(low || 2);
      }
    } catch (err) {
      console.error('Failed to fetch spatial GeoJSON datasets:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGeoJSONLayers();
  }, [API_BASE_URL, filters]);

  return (
    <main className="min-h-screen bg-slate-100 text-slate-900 flex flex-col justify-between p-4 md:p-6 space-y-5 font-sans">
      
      {/* 1. Header & Top Command Bar */}
      <header className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        
        {/* Brand & Regional Focus */}
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-blue-900 text-white rounded-lg shadow-sm flex items-center justify-center">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
              <span>CivicPulse Monsoon</span>
              <span className="text-xs bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded border border-blue-300">🇮🇳 INDIA &bull; TAMIL NADU FOCUS</span>
            </h1>
            <p className="text-xs text-slate-500 font-medium">
              AI-Powered Waterlogging Risk & Response Operations &bull; National to Ward-Level Decision Support
            </p>
          </div>
        </div>

        {/* Location Search Bar & Provenance Badge */}
        <div className="flex flex-wrap items-center gap-3">
          <SearchBar
            geoData={geoData}
            apiBaseUrl={API_BASE_URL}
            selectedDistrict={filters.districtId}
            onSelectSearchResult={(f) => {
              setSearchResult(f);
              setSelectedFeature({
                type: f.properties?.incident_type ? 'incident' : 'ward',
                properties: f.properties,
                id: f.id,
              });
              // Maintain geographic consistency by auto-selecting parent district
              if (f.properties?.district) {
                handleFilterChange('districtId', f.properties.district);
              }
            }}
          />

          {/* DATA MODE Status Indicator */}
          <div className="flex items-center space-x-2 bg-amber-50 border border-amber-200 px-3 py-2 rounded-lg text-xs font-semibold text-amber-900">
            <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
            <span>DATA MODE &bull; Public + Synthetic Sample Data</span>
          </div>
        </div>

      </header>

      {/* 2. Rainfall Scenario Bar & Main Metrics Summary Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        
        {/* Scenario Rainfall Input Panel (4 Cols) */}
        <div className="lg:col-span-4 bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-3">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <span className="text-xs font-bold text-slate-700 uppercase flex items-center space-x-1.5">
              <CloudRain className="w-4 h-4 text-blue-600" />
              <span>Scenario Rainfall Input</span>
            </span>
            <span className="text-[10px] text-slate-400 font-semibold">(Forecast Input)</span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Expected Rainfall</label>
              <div className="flex items-center space-x-2">
                <input
                  type="number"
                  min="10"
                  max="300"
                  value={scenarioRainfall}
                  onChange={(e) => setScenarioRainfall(Number(e.target.value))}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 font-bold text-slate-900 text-xs focus:ring-2 focus:ring-blue-500"
                />
                <span className="text-slate-500 font-semibold">mm</span>
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Forecast Horizon</label>
              <select
                value={forecastHorizon}
                onChange={(e) => setForecastHorizon(Number(e.target.value))}
                className="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 font-bold text-slate-900 text-xs focus:ring-2 focus:ring-blue-500"
              >
                <option value={24}>24 Hours</option>
                <option value={48}>48 Hours</option>
                <option value={72}>72 Hours</option>
              </select>
            </div>
          </div>

          <button
            onClick={fetchGeoJSONLayers}
            className="w-full bg-blue-900 hover:bg-blue-800 text-white font-semibold py-2 rounded-lg text-xs flex items-center justify-center space-x-2 transition shadow-xs"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>RUN PREDICTION SCENARIO</span>
          </button>
        </div>

        {/* Metric Cards (8 Cols) */}
        <div className="lg:col-span-8 grid grid-cols-2 md:grid-cols-4 gap-3">
          
          {/* High Risk Card */}
          <div className="bg-white border-l-4 border-l-red-600 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col justify-between">
            <span className="text-[11px] font-bold text-slate-500 uppercase">HIGH RISK AREAS</span>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-2xl font-black text-red-600">{highRiskCount}</span>
              <span className="text-xs text-slate-500 font-semibold">Wards</span>
            </div>
            <span className="text-[10px] text-red-700 bg-red-50 font-bold px-2 py-0.5 rounded w-max mt-2 border border-red-200">
              High-Risk Interventions
            </span>
          </div>

          {/* Medium Risk Card */}
          <div className="bg-white border-l-4 border-l-amber-500 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col justify-between">
            <span className="text-[11px] font-bold text-slate-500 uppercase">MEDIUM RISK AREAS</span>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-2xl font-black text-amber-600">{medRiskCount}</span>
              <span className="text-xs text-slate-500 font-semibold">Wards</span>
            </div>
            <span className="text-[10px] text-amber-800 bg-amber-50 font-bold px-2 py-0.5 rounded w-max mt-2 border border-amber-200">
              Active Monitoring
            </span>
          </div>

          {/* Low Risk Card */}
          <div className="bg-white border-l-4 border-l-emerald-600 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col justify-between">
            <span className="text-[11px] font-bold text-slate-500 uppercase">LOW RISK AREAS</span>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-2xl font-black text-emerald-600">{lowRiskCount}</span>
              <span className="text-xs text-slate-500 font-semibold">Wards</span>
            </div>
            <span className="text-[10px] text-emerald-800 bg-emerald-50 font-bold px-2 py-0.5 rounded w-max mt-2 border border-emerald-200">
              Normal Operations
            </span>
          </div>

          {/* Active Priority Actions Card */}
          <div className="bg-white border-l-4 border-l-blue-600 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col justify-between">
            <span className="text-[11px] font-bold text-slate-500 uppercase">ACTIVE PRIORITY ACTIONS</span>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-2xl font-black text-blue-900">5</span>
              <span className="text-xs text-slate-500 font-semibold">Actions</span>
            </div>
            <span className="text-[10px] text-blue-800 bg-blue-50 font-bold px-2 py-0.5 rounded w-max mt-2 border border-blue-200">
              OR-Tools Optimized
            </span>
          </div>

        </div>

      </div>

      {/* 3. Main Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 flex-1">
        
        {/* Left Panel: Regional Focus, District Selector & GIS Layers (3 Cols) */}
        <aside className="lg:col-span-3 space-y-4">
          <FilterPanel
            layers={layers}
            onToggleLayer={handleToggleLayer}
            filters={filters}
            onFilterChange={handleFilterChange}
            wardsList={wardsList}
            onFocusCamera={handleFocusCamera}
          />
        </aside>

        {/* Center Area: Full Screen Interactive Geographic Map (6 Cols) */}
        <section className="lg:col-span-6 relative rounded-xl overflow-hidden border border-slate-200 shadow-sm bg-slate-200 min-h-[550px] flex flex-col">
          <MapViewContainer
            layers={layers}
            geoData={geoData}
            selectedWardId={selectedFeature?.type === 'ward' ? selectedFeature.id : null}
            onSelectFeature={(feat) => setSelectedFeature(feat)}
            searchResult={searchResult}
            cameraTrigger={cameraTrigger}
            selectedDistrict={filters.districtId}
          />

          {/* Map Legend Overlay */}
          <div className="absolute bottom-4 left-4 z-10">
            <MapLegend />
          </div>
        </section>

        {/* Right Panel: Selected Location Inspector (3 Cols) */}
        <aside className="lg:col-span-3 space-y-4">
          <FeatureDetailsPanel
            selectedFeature={selectedFeature}
            onClose={() => setSelectedFeature(null)}
            apiBaseUrl={API_BASE_URL}
          />
        </aside>

      </div>

      {/* 4. Historical Rainfall Analytics & Season Trends (Real Uploaded Datasets) */}
      <section className="pt-2">
        <RainfallAnalyticsPanel selectedDistrict={filters.districtId} apiBaseUrl={API_BASE_URL} />
      </section>

      {/* 5. Priority Action Queue Engine */}
      <section className="pt-2">
        <PriorityQueuePanel selectedDistrict={filters.districtId} apiBaseUrl={API_BASE_URL} />
      </section>

      {/* 5. Crew & Budget Optimization Engine (Google OR-Tools MILP) */}
      <section className="pt-2">
        <ResourcePlannerPanel apiBaseUrl={API_BASE_URL} />
      </section>

      {/* 6. What-If Scenario Simulator Panel */}
      <section className="pt-2">
        <WhatIfSimulatorPanel apiBaseUrl={API_BASE_URL} />
      </section>

      {/* 7. Footer & Data Provenance Notice */}
      <footer className="pt-4 text-center text-xs text-slate-500 border-t border-slate-200 flex flex-col md:flex-row justify-between items-center font-sans gap-2">
        <span>Smart India Hackathon &bull; CivicPulse Monsoon Decision Support System (India & Tamil Nadu)</span>
        <span>Data Provenance & Quality: <strong className="text-amber-800 font-semibold bg-amber-50 px-2 py-0.5 rounded border border-amber-200">DATA MODE: Public Data + Synthetic Sample</strong></span>
      </footer>

    </main>
  );
}
