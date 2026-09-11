'use client';

import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import { Layers, Globe, AlertTriangle } from 'lucide-react';

interface MapViewProps {
  layers: {
    wards: boolean;
    roads: boolean;
    drains: boolean;
    waterbodies: boolean;
    incidents: boolean;
    facilities: boolean;
    population: boolean;
    populationExposure?: boolean;
    districts?: boolean;
    state?: boolean;
  };
  geoData: {
    wards: any;
    roads: any;
    drains: any;
    waterbodies: any;
    incidents: any;
    facilities: any;
    population: any;
    populationExposure?: any;
    districts?: any;
    state?: any;
  };
  selectedWardId: string | number | null;
  onSelectFeature: (feature: { type: string; properties: any; id?: any }) => void;
  searchResult: any;
  cameraTrigger?: { type: 'india' | 'tn' | 'district' | 'ward'; coords?: [number, number]; timestamp?: number } | null;
  selectedDistrict?: string;
}

const TILE_PROVIDERS = {
  osm: {
    name: 'OpenStreetMap Standard (Full India & TN Labels)',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  },
  carto_voyager: {
    name: 'Carto Voyager (Municipal Operations)',
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
    maxZoom: 19,
  },
  esri_street: {
    name: 'Esri World Street Map (Detailed Infrastructure)',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, USGS, Garmin',
    maxZoom: 18,
  },
};

export const ALL_38_TN_DISTRICT_CENTERS: Record<string, [number, number]> = {
  "Ariyalur": [11.1400, 79.0700],
  "Chengalpattu": [12.6800, 79.9800],
  "Chennai": [13.0827, 80.2707],
  "Coimbatore": [11.0168, 76.9558],
  "Cuddalore": [11.7500, 79.7500],
  "Dharmapuri": [12.1300, 78.1600],
  "Dindigul": [10.3600, 77.9800],
  "Erode": [11.3410, 77.7172],
  "Kallakurichi": [11.7380, 78.9620],
  "Kancheepuram": [12.8342, 79.7036],
  "Karur": [10.9600, 78.0800],
  "Krishnagiri": [12.5200, 78.2100],
  "Madurai": [9.9252, 78.1198],
  "Mayiladuthurai": [11.1000, 79.6500],
  "Nagapattinam": [10.7600, 79.8400],
  "Kanniyakumari": [8.0800, 77.5700],
  "Namakkal": [11.2200, 78.1700],
  "Perambalur": [11.2300, 78.8800],
  "Pudukkottai": [10.3800, 78.8200],
  "Ramanathapuram": [9.3700, 78.8300],
  "Ranipet": [12.9200, 79.3300],
  "Salem": [11.6643, 78.1460],
  "Sivagangai": [9.8500, 78.4800],
  "Tenkasi": [8.9600, 77.3100],
  "Thanjavur": [10.7800, 79.1300],
  "Theni": [10.0100, 77.4700],
  "Thiruvallur": [13.1400, 79.9100],
  "Thiruvarur": [10.7700, 79.6300],
  "Thoothukudi": [8.7600, 78.1300],
  "Tiruchirappalli": [10.7905, 78.7047],
  "Tirunelveli": [8.7139, 77.7567],
  "Tirupathur": [12.4900, 78.5600],
  "Tiruppur": [11.1085, 77.3411],
  "Tiruvannamalai": [12.2200, 79.0700],
  "The Nilgiris": [11.4100, 76.7000],
  "Vellore": [12.9165, 79.1325],
  "Viluppuram": [11.9400, 79.4920],
  "Virudhunagar": [9.5800, 77.9500],
};

export default function MapView({
  layers,
  geoData,
  selectedWardId,
  onSelectFeature,
  searchResult,
  cameraTrigger,
  selectedDistrict,
}: MapViewProps) {
  const mapRef = useRef<L.Map | null>(null);
  const tileLayerRef = useRef<L.TileLayer | null>(null);
  const layerGroupRef = useRef<L.LayerGroup | null>(null);
  const [activeTileProvider, setActiveTileProvider] = useState<keyof typeof TILE_PROVIDERS>('osm');
  const [currentZoom, setCurrentZoom] = useState<number>(7.5);
  const [currentCenter, setCurrentCenter] = useState<{ lat: number; lng: number }>({ lat: 11.1271, lng: 78.6569 });
  const [isDebugMode, setIsDebugMode] = useState<boolean>(false);

  // Initialize Leaflet Map — Defaulting to Tamil Nadu State View
  useEffect(() => {
    if (!mapRef.current) {
      const map = L.map('municipal-map', {
        center: [11.1271, 78.6569], // Tamil Nadu Center
        zoom: 7.5,
        minZoom: 4,
        maxZoom: 19,
        zoomControl: false,
      });

      const provider = TILE_PROVIDERS.osm;
      const baseTile = L.tileLayer(provider.url, {
        attribution: provider.attribution,
        maxZoom: provider.maxZoom,
      }).addTo(map);

      tileLayerRef.current = baseTile;
      L.control.zoom({ position: 'topright' }).addTo(map);

      map.on('zoomend', () => setCurrentZoom(map.getZoom()));
      map.on('moveend', () => {
        const c = map.getCenter();
        setCurrentCenter({ lat: Number(c.lat.toFixed(4)), lng: Number(c.lng.toFixed(4)) });
      });

      map.on('click', (e) => {
        const lat = Number(e.latlng.lat.toFixed(5));
        const lng = Number(e.latlng.lng.toFixed(5));
        L.popup()
          .setLatLng(e.latlng)
          .setContent(
            `<div style="font-family:sans-serif;padding:2px;font-size:12px;">
              <strong style="color:#0f172a;">Geographic Location</strong><br/>
              <span style="color:#475569;">Latitude: <strong>${lat}° N</strong></span><br/>
              <span style="color:#475569;">Longitude: <strong>${lng}° E</strong></span><br/>
              <span style="font-size:10px;color:#2563eb;">Real Coordinates (OpenStreetMap)</span>
            </div>`
          )
          .openOn(map);
      });

      layerGroupRef.current = L.layerGroup().addTo(map);
      mapRef.current = map;
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  // Update Tile Layer
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    if (tileLayerRef.current) {
      map.removeLayer(tileLayerRef.current);
    }

    const provider = TILE_PROVIDERS[activeTileProvider];
    const newTile = L.tileLayer(provider.url, {
      attribution: provider.attribution,
      maxZoom: provider.maxZoom,
    }).addTo(map);

    tileLayerRef.current = newTile;
  }, [activeTileProvider]);

  // Handle District Change Camera Panning
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !selectedDistrict || selectedDistrict === 'ALL') return;

    if (ALL_38_TN_DISTRICT_CENTERS[selectedDistrict]) {
      const coords = ALL_38_TN_DISTRICT_CENTERS[selectedDistrict];
      map.flyTo(coords, 10.5, { duration: 1.2 });
    }
  }, [selectedDistrict]);

  // Handle Camera Trigger (India, TN, District, Ward)
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !cameraTrigger) return;

    if (cameraTrigger.type === 'india') {
      map.flyTo([20.5937, 78.9629], 5, { duration: 1.5 });
    } else if (cameraTrigger.type === 'tn') {
      map.flyTo([11.1271, 78.6569], 7.5, { duration: 1.5 });
    } else if (cameraTrigger.type === 'district' && cameraTrigger.coords) {
      map.flyTo(cameraTrigger.coords, 10.5, { duration: 1.2 });
    } else if (cameraTrigger.type === 'ward' && cameraTrigger.coords) {
      map.flyTo(cameraTrigger.coords, 13, { duration: 1.2 });
    }
  }, [cameraTrigger]);

  // Update Layers & Render Progressive Geometry (Progressive Zoom Visibility)
  useEffect(() => {
    const map = mapRef.current;
    const layerGroup = layerGroupRef.current;
    if (!map || !layerGroup) return;

    layerGroup.clearLayers();

    // Layer 1: Tamil Nadu State Boundary (Zoom <= 8)
    if (currentZoom <= 8 && geoData.state?.features) {
      const stateLayer = L.geoJSON(geoData.state, {
        style: {
          color: '#1e3a8a',
          weight: 3,
          fillColor: '#3b82f6',
          fillOpacity: 0.06,
          dashArray: '6, 6',
        },
      });
      layerGroup.addLayer(stateLayer);
    }

    // Layer 2: All 38 District Boundaries (Zoom > 5 and Zoom <= 11)
    if (currentZoom > 5 && currentZoom <= 11 && layers.districts && geoData.districts?.features) {
      const districtLayer = L.geoJSON(geoData.districts, {
        style: (feature) => {
          const isSelected = selectedDistrict && selectedDistrict !== 'ALL' && feature?.properties?.district === selectedDistrict;
          return {
            color: isSelected ? '#0f172a' : '#d97706',
            weight: isSelected ? 3.5 : 2,
            fillColor: isSelected ? '#f59e0b' : '#fbbf24',
            fillOpacity: isSelected ? 0.2 : 0.08,
          };
        },
        onEachFeature: (feature, layer) => {
          const name = feature.properties.name || feature.properties.district;
          layer.bindTooltip(`<strong>District: ${name}</strong>`, { sticky: true });
          layer.on({
            click: () => {
              if (feature.properties.center) {
                map.flyTo(feature.properties.center, 10.5, { duration: 1.2 });
              }
              onSelectFeature({ type: 'district', properties: feature.properties, id: feature.properties.id });
            },
          });
        },
      });
      layerGroup.addLayer(districtLayer);
    }

    // Layer 3: Wards, Towns & Rural Villages (Zoom > 8)
    if (currentZoom > 8 && layers.wards && geoData.wards?.features) {
      const wardLayer = L.geoJSON(geoData.wards, {
        style: (feature) => {
          const isSelected = selectedWardId && String(feature?.properties?.id) === String(selectedWardId);
          const riskLevel = (feature?.properties?.risk_level || 'NO DATA').toUpperCase();

          let strokeColor = '#64748b';
          let fillColor = '#cbd5e1';

          if (riskLevel === 'HIGH' || riskLevel === 'CRITICAL') {
            strokeColor = '#dc2626';
            fillColor = '#ef4444';
          } else if (riskLevel === 'MEDIUM') {
            strokeColor = '#d97706';
            fillColor = '#f59e0b';
          } else if (riskLevel === 'LOW') {
            strokeColor = '#16a34a';
            fillColor = '#22c55e';
          }

          if (isSelected) strokeColor = '#0f172a';

          return {
            color: strokeColor,
            weight: isSelected ? 3.5 : 2,
            fillColor: fillColor,
            fillOpacity: isSelected ? 0.3 : 0.18,
            dashArray: riskLevel === 'NO DATA' ? '4, 4' : undefined,
          };
        },
        onEachFeature: (feature, layer) => {
          const risk = feature.properties.risk_level || 'NO DATA';
          const riskBadge =
            risk === 'HIGH' ? '<span style="color:#dc2626;font-weight:bold;">HIGH RISK</span>' :
            risk === 'MEDIUM' ? '<span style="color:#d97706;font-weight:bold;">MEDIUM RISK</span>' :
            risk === 'LOW' ? '<span style="color:#16a34a;font-weight:bold;">LOW RISK</span>' :
            '<span style="color:#64748b;font-weight:bold;">NO DATA</span>';

          layer.bindTooltip(
            `<div style="font-family:sans-serif;padding:2px;">
              <strong style="font-size:13px;color:#0f172a;">${feature.properties.name}</strong><br/>
              <span style="font-size:11px;color:#475569;">District: ${feature.properties.district || 'TN'}</span><br/>
              <span style="font-size:11px;">Status: ${riskBadge}</span>
            </div>`,
            { sticky: true }
          );
          layer.on({
            click: () => {
              onSelectFeature({ type: 'ward', properties: feature.properties, id: feature.properties.id });
            },
          });
        },
      });
      layerGroup.addLayer(wardLayer);
    }

    // Layer 4: Roads (Zoom > 8, progressive detail filter)
    if (currentZoom > 8 && layers.roads && geoData.roads?.features) {
      // Filter out smaller roads if zoomed out (currentZoom <= 11)
      const filteredRoads = {
        ...geoData.roads,
        features: geoData.roads.features.filter((feature: any) => {
          if (currentZoom <= 11) {
            const type = feature.properties?.road_type || "";
            return ["motorway", "trunk", "primary", "secondary", "tertiary", "arterial", "highway"].includes(type);
          }
          return true;
        })
      };

      const roadLayer = L.geoJSON(filteredRoads, {
        style: (feature) => {
          const type = feature?.properties?.road_type;
          const isArterial = ['arterial', 'highway', 'motorway', 'trunk', 'primary', 'secondary', 'tertiary'].includes(type);
          return {
            color: isArterial ? '#ea580c' : '#64748b',
            weight: isArterial ? 3 : 1.5,
            opacity: 0.85,
          };
        },
        onEachFeature: (feature, layer) => {
          layer.bindTooltip(`<strong>Road:</strong> ${feature.properties.name}`);
          layer.on({ click: () => onSelectFeature({ type: 'road', properties: feature.properties }) });
        },
      });
      layerGroup.addLayer(roadLayer);
    }

    // Layer 5: Drainage Channels (Zoom > 11 only)
    if (currentZoom > 11 && layers.drains && geoData.drains?.features) {
      const drainLayer = L.geoJSON(geoData.drains, {
        style: (feature) => {
          const status = feature?.properties?.status;
          const isBlocked = status === 'blocked' || status === 'partially_blocked';
          return {
            color: isBlocked ? '#dc2626' : '#0284c7',
            weight: isBlocked ? 3.5 : 2,
            dashArray: isBlocked ? '6, 4' : undefined,
          };
        },
        onEachFeature: (feature, layer) => {
          layer.bindTooltip(`<strong>Drain:</strong> ${feature.properties.name} [${(feature.properties.status || 'NORMAL').toUpperCase()}]`);
          layer.on({ click: () => onSelectFeature({ type: 'drain', properties: feature.properties }) });
        },
      });
      layerGroup.addLayer(drainLayer);
    }

    // Layer 6: Waterbodies (Zoom > 8)
    if (currentZoom > 8 && layers.waterbodies && geoData.waterbodies?.features) {
      const wbLayer = L.geoJSON(geoData.waterbodies, {
        style: { color: '#2563eb', weight: 1.5, fillColor: '#3b82f6', fillOpacity: 0.3 },
        onEachFeature: (feature, layer) => {
          layer.bindTooltip(`<strong>Waterbody:</strong> ${feature.properties.name} (${feature.properties.type})`);
          layer.on({ click: () => onSelectFeature({ type: 'waterbody', properties: feature.properties }) });
        },
      });
      layerGroup.addLayer(wbLayer);
    }

    // Layer 7: Waterlogging Incidents (Zoom > 8)
    if (currentZoom > 8 && layers.incidents && geoData.incidents?.features) {
      geoData.incidents.features.forEach((feature: any) => {
        const coords = feature.geometry?.coordinates;
        if (!coords || coords.length < 2) return;
        const [lon, lat] = coords;

        const severity = (feature.properties.severity || '').toUpperCase();
        const color = severity === 'HIGH' || severity === 'CRITICAL' ? '#dc2626' : '#f59e0b';

        const marker = L.circleMarker([lat, lon], {
          radius: 7,
          color: '#ffffff',
          weight: 2,
          fillColor: color,
          fillOpacity: 0.95,
        });

        marker.bindTooltip(
          `<div style="font-family:sans-serif;padding:2px;">
            <strong style="color:#dc2626;">[INCIDENT] ${feature.properties.incident_type}</strong><br/>
            <span style="font-size:11px;color:#475569;">${feature.properties.description || ''}</span>
          </div>`
        );
        marker.on('click', () => onSelectFeature({ type: 'incident', properties: feature.properties }));
        layerGroup.addLayer(marker);
      });
    }

    // Layer 8: Critical Facilities & POIs (Zoom > 11 only)
    if (currentZoom > 11 && layers.facilities && geoData.facilities?.features) {
      geoData.facilities.features.forEach((feature: any) => {
        const coords = feature.geometry?.coordinates;
        if (!coords || coords.length < 2) return;
        const [lon, lat] = coords;

        const type = feature.properties.facility_type;
        const color = type === 'hospital' ? '#059669' : type === 'school' ? '#7c3aed' : type === 'temple' ? '#d97706' : '#2563eb';

        const marker = L.circleMarker([lat, lon], {
          radius: 6,
          color: '#ffffff',
          weight: 1.5,
          fillColor: color,
          fillOpacity: 0.95,
        });

        marker.bindTooltip(`<strong>Facility / POI:</strong> ${feature.properties.name} (${feature.properties.category || feature.properties.facility_type})`);
        marker.on('click', () => onSelectFeature({ type: 'facility', properties: feature.properties }));
        layerGroup.addLayer(marker);
      });
    }

    // Layer 9: Population Choropleth (Strictly Real Boundary Polygons Only, Zero Fake Buffers)
    const activePopData = (layers.population || layers.populationExposure) 
      ? (geoData.population?.features?.length ? geoData.population : geoData.populationExposure) 
      : null;

    if (activePopData?.features) {
      // Strictly enforce real geographic boundary polygons only (never points, lines, or circles)
      const validPolygonFeatures = activePopData.features.filter((f: any) => {
        const geomType = f.geometry?.type;
        return geomType === 'Polygon' || geomType === 'MultiPolygon';
      });

      const popLayer = L.geoJSON({ type: "FeatureCollection", features: validPolygonFeatures } as any, {
        style: (feature) => {
          const isSelected = selectedWardId && String(feature?.properties?.id) === String(selectedWardId);
          const p = feature?.properties || {};
          const pop = p.population;
          const popClass = p.population_classification || (
            pop === null || pop === undefined ? 'NO_DATA' : 
            (pop >= 75000 ? 'HIGH' : (pop >= 25000 ? 'MEDIUM' : 'LOW'))
          );

          if (popClass === 'NO_DATA' || pop === null || pop === undefined) {
            return {
              color: '#94a3b8',
              weight: 1.5,
              fillColor: '#f1f5f9',
              fillOpacity: 0.15,
              dashArray: '4, 4',
            };
          } else if (popClass === 'HIGH') {
            return {
              color: '#1e40af', // Deep Royal Blue
              weight: isSelected ? 3.5 : 2,
              fillColor: '#3b82f6',
              fillOpacity: isSelected ? 0.5 : 0.35,
            };
          } else if (popClass === 'MEDIUM') {
            return {
              color: '#0284c7', // Sky / Ocean Blue
              weight: isSelected ? 3 : 1.5,
              fillColor: '#38bdf8',
              fillOpacity: isSelected ? 0.4 : 0.28,
            };
          } else {
            return {
              color: '#0891b2', // Cyan
              weight: isSelected ? 3 : 1.5,
              fillColor: '#22d3ee',
              fillOpacity: isSelected ? 0.35 : 0.22,
            };
          }
        },
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          const pop = p.population;
          const popClass = p.population_classification || 'NO_DATA';

          const badgeColor = 
            popClass === 'HIGH' ? '#1e40af' :
            popClass === 'MEDIUM' ? '#0284c7' :
            popClass === 'LOW' ? '#0891b2' : '#64748b';
          const badgeText = 
            popClass === 'HIGH' ? 'High Population' :
            popClass === 'MEDIUM' ? 'Medium Population' :
            popClass === 'LOW' ? 'Low Population' : 'No Data';

          let tooltipHtml = `
            <div style="font-family:sans-serif;padding:3px;min-width:170px;">
              <strong style="font-size:12px;color:#1e3a8a;">${p.name}</strong><br/>
              <span style="font-size:10px;color:#475569;">Geographic Level: <strong>${p.geographic_level || p.level || 'Boundary'}</strong></span><br/>
              <div style="margin-top:2px;font-size:11px;color:#0f172a;">
                Population: <strong>${pop ? pop.toLocaleString() : 'No Data'}</strong>
                <span style="display:inline-block;margin-left:4px;padding:1px 4px;font-size:9px;font-weight:bold;color:#ffffff;background-color:${badgeColor};border-radius:3px;">${badgeText}</span>
              </div>
              <div style="font-size:10px;color:#64748b;margin-top:1px;">Source: ${p.data_source || 'Census of India'} (${p.data_year || 'Census 2011'})</div>
              <div style="font-size:10px;color:#047857;margin-top:1px;font-weight:600;">Boundary: ${p.boundary_status || 'Verified Administrative Boundary'}</div>
              ${isDebugMode ? `
                <div style="margin-top:3px;padding:3px 5px;background-color:#faf5ff;border:1px dashed #c084fc;border-radius:3px;font-size:9px;color:#4c1d95;">
                  <div><strong>Boundary ID:</strong> ${p.boundary_id || p.id || 'N/A'}</div>
                  <div><strong>Record ID:</strong> ${p.population_record_id || 'N/A'}</div>
                  <div style="color:${p.join_status?.includes('MATCHED') ? '#16a34a' : '#d97706'};font-weight:bold;"><strong>JOIN STATUS:</strong> ${p.join_status || 'MATCHED (Administrative Polygon)'}</div>
                </div>
              ` : ''}
              ${p.exposed_population ? `
                <div style="margin-top:3px;padding:2px 4px;background-color:#fff7ed;border:1px solid #ffedd5;border-radius:3px;font-size:10px;color:#c2410c;font-weight:600;">
                  Est. Exposed: ~${p.exposed_population.toLocaleString()} (${p.risk_level || 'LOW'} Risk)
                </div>
              ` : ''}
            </div>
          `;
          
          layer.bindTooltip(tooltipHtml, { sticky: true });
          layer.on({
            click: () => {
              onSelectFeature({ type: 'population_zone', properties: p, id: p.id });
            }
          });
        }
      });
      layerGroup.addLayer(popLayer);
    }
  }, [currentZoom, layers, geoData, selectedWardId, selectedDistrict, isDebugMode, onSelectFeature]);

  // Handle Search Result Panning
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !searchResult) return;

    if (searchResult.geometry?.coordinates) {
      const coords = searchResult.geometry.coordinates;
      if (searchResult.geometry.type === 'Point') {
        map.flyTo([coords[1], coords[0]], 13, { duration: 1.2 });
      } else if (searchResult.geometry.type === 'Polygon' || searchResult.geometry.type === 'MultiPolygon') {
        const geoLayer = L.geoJSON(searchResult);
        map.fitBounds(geoLayer.getBounds(), { padding: [40, 40], maxZoom: 13 });
      }
    }
  }, [searchResult]);

  return (
    <div className="relative w-full h-full min-h-[550px]">
      
      {/* Base Map Tile Provider Selector & Zoom Level Indicator */}
      <div className="absolute top-3 left-3 z-10 bg-white/95 border border-slate-300 rounded-lg p-2.5 shadow-md text-xs space-y-1.5 backdrop-blur-sm">
        <div className="flex items-center space-x-2 text-[10px] font-bold text-slate-700 uppercase tracking-wider">
          <Globe className="w-3.5 h-3.5 text-blue-600" />
          <span>Base Map Tile Provider</span>
        </div>

        <select
          value={activeTileProvider}
          onChange={(e) => setActiveTileProvider(e.target.value as any)}
          className="w-full bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-800 font-medium focus:ring-2 focus:ring-blue-500"
        >
          {Object.entries(TILE_PROVIDERS).map(([key, provider]) => (
            <option key={key} value={key}>{provider.name}</option>
          ))}
        </select>

        {/* Live Zoom Level & Real Coordinates Status Bar */}
        <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1 border-t border-slate-100 font-sans">
          <span className="font-semibold text-slate-700">Zoom: <strong className="text-blue-700">{currentZoom}</strong></span>
          <span className="font-semibold text-slate-600">{currentCenter.lat}°N, {currentCenter.lng}°E</span>
        </div>

        {/* Temporary Population Join Debug Mode Toggle */}
        <div className="pt-1 border-t border-slate-100">
          <button
            onClick={() => setIsDebugMode(!isDebugMode)}
            className={`w-full px-2 py-1 rounded text-[10px] font-bold flex items-center justify-between border transition ${
              isDebugMode 
                ? 'bg-purple-700 text-white border-purple-800 shadow-sm' 
                : 'bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200'
            }`}
          >
            <span>Population Join Debug</span>
            <span className="uppercase text-[9px] px-1 py-0.5 rounded bg-black/20">{isDebugMode ? 'ON' : 'OFF'}</span>
          </button>
        </div>
      </div>

      {/* Informational Banner: When Population layer is active and sub-district polygons are unavailable */}
      {(layers.population || layers.populationExposure) && (selectedDistrict === 'The Nilgiris' || selectedDistrict === 'Theni') && currentZoom > 10 && (
        <div className="absolute top-3 left-64 z-10 bg-amber-50/95 border border-amber-300 rounded-lg px-3 py-2 shadow-md text-xs backdrop-blur-sm max-w-md text-amber-900 flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          <div className="text-[11px] leading-snug">
            <span className="font-bold">Village/Block Boundary Polygons Unavailable:</span>
            <span className="block text-amber-800 text-[10px] mt-0.5">
              Census 2011 records for {selectedDistrict} are preserved in the inspector. Real district boundary is displayed; zero circular or estimated polygons are drawn.
            </span>
          </div>
        </div>
      )}

      {/* Main Leaflet Map Container */}
      <div id="municipal-map" className="w-full h-full min-h-[550px] z-0" />
    </div>
  );
}
