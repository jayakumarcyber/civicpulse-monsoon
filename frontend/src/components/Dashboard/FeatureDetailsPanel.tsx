'use client';

import { useState, useEffect } from 'react';
import { X, Building2, AlertTriangle, ShieldAlert, Database, MapPin, Users } from 'lucide-react';
import RiskCard from '@/components/XAI/RiskCard';

interface FeatureDetailsProps {
  selectedFeature: {
    type: string;
    properties: any;
    id?: any;
  } | null;
  onClose: () => void;
  apiBaseUrl: string;
}

export default function FeatureDetailsPanel({
  selectedFeature,
  onClose,
  apiBaseUrl,
}: FeatureDetailsProps) {
  const [wardMetrics, setWardMetrics] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (selectedFeature && selectedFeature.type === 'ward' && selectedFeature.id) {
      setLoading(true);
      fetch(`${apiBaseUrl}/api/v1/wards/${selectedFeature.id}/metrics`)
        .then((res) => res.json())
        .then((data) => setWardMetrics(data))
        .catch(() => setWardMetrics(null))
        .finally(() => setLoading(false));
    } else {
      setWardMetrics(null);
    }
  }, [selectedFeature, apiBaseUrl]);

  if (!selectedFeature) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-6 text-center text-slate-500 text-xs font-sans shadow-sm">
        <MapPin className="w-8 h-8 mx-auto mb-2 text-slate-400" />
        <p className="font-medium text-slate-700">SELECTED AREA INSPECTOR</p>
        <p className="text-slate-500 text-[11px] mt-1">Select any ward or location on the map to inspect waterlogging risk, exposure, and priority actions.</p>
      </div>
    );
  }

  const p = selectedFeature.properties || {};

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4 text-xs font-sans relative">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <div>
          <span className="text-[10px] uppercase font-bold text-blue-700 tracking-wider">
            {selectedFeature.type.replace('_', ' ')} Inspector
          </span>
          <h2 className="text-base font-bold text-slate-900">
            {p.name || p.zone_name || p.incident_id || `Feature #${p.id || 'N/A'}`}
          </h2>
          {p.city && <span className="text-xs text-slate-500 font-medium">City: {p.city}</span>}
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg bg-slate-100 text-slate-500 hover:text-slate-900 hover:bg-slate-200 transition"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Data Source Quality & Status Badge */}
      <div className="bg-slate-50 border border-slate-200 p-2.5 rounded-lg flex flex-col gap-1.5 text-[11px] font-sans">
        <div className="flex justify-between items-center">
          <span className="text-slate-600 font-medium">Data Source:</span>
          <span className="text-blue-900 font-bold bg-blue-50 px-2 py-0.5 rounded border border-blue-200 text-[10px]">
            {p.data_source_type || p.data_source || 'OpenStreetMap Public Data'}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-600 font-medium">Data Status:</span>
          <span className="text-amber-900 font-bold bg-amber-50 px-2 py-0.5 rounded border border-amber-200 text-[10px]">
            {p.data_status || 'Verified / Public Data'}
          </span>
        </div>
      </div>

      {/* Ward Details & Metrics */}
      {selectedFeature.type === 'ward' && (
        <div className="space-y-4">
          {loading ? (
            <p className="text-slate-400 text-xs animate-pulse">Loading spatial exposure metrics...</p>
          ) : wardMetrics ? (
            <div>
              <h3 className="text-[11px] font-bold text-slate-700 uppercase mb-2">Population & Infrastructure Exposure</h3>
              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
                  <span className="text-slate-500 block text-[10px]">Population Exposure</span>
                  <span className="font-bold text-slate-900">{wardMetrics.population?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
                  <span className="text-slate-500 block text-[10px]">Area Size</span>
                  <span className="font-bold text-slate-900">{wardMetrics.area_sq_km || 'N/A'} sq km</span>
                </div>
                <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
                  <span className="text-slate-500 block text-[10px]">Hospitals / Schools</span>
                  <span className="font-bold text-emerald-700">{wardMetrics.facilities_count} facilities</span>
                </div>
                <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
                  <span className="text-slate-500 block text-[10px]">Drainage Outfalls</span>
                  <span className="font-bold text-blue-700">{wardMetrics.drains_count} drains</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-center text-[11px] text-red-900 font-semibold flex items-center justify-center space-x-1.5">
              <AlertTriangle className="w-4 h-4 text-red-600 shrink-0" />
              <span>Detailed locality data unavailable</span>
            </div>
          )}

          {/* Explainable Risk Prediction Engine */}
          <RiskCard wardId={selectedFeature.id} wardName={p.name || 'Ward'} apiBaseUrl={apiBaseUrl} />
        </div>
      )}

      {/* Incident Details */}
      {selectedFeature.type === 'incident' && (
        <div className="space-y-2 text-xs">
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Incident Type:</span>
            <span className="text-red-700 font-bold uppercase">{p.incident_type}</span>
          </div>
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Severity:</span>
            <span className="text-amber-700 font-bold uppercase">{p.severity}</span>
          </div>
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Status:</span>
            <span className="text-slate-800 font-medium">{p.status}</span>
          </div>
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Reported At:</span>
            <span className="text-slate-700">{p.reported_at ? new Date(p.reported_at).toLocaleString() : 'N/A'}</span>
          </div>
          <p className="text-slate-700 pt-2 bg-slate-50 p-2.5 rounded-lg border border-slate-200 italic">{p.description || 'No description provided.'}</p>
        </div>
      )}

      {/* Drain Details */}
      {selectedFeature.type === 'drain' && (
        <div className="space-y-2 text-xs">
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Drain Classification:</span>
            <span className="text-sky-700 font-bold">{p.drain_type}</span>
          </div>
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Capacity:</span>
            <span className="text-slate-800 font-medium">{p.capacity || 'N/A'}</span>
          </div>
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Operational Status:</span>
            <span className={`font-bold ${p.status === 'blocked' ? 'text-red-700' : 'text-emerald-700'}`}>
              {(p.status || 'UNKNOWN').toUpperCase()}
            </span>
          </div>
        </div>
      )}

      {/* Facility Details */}
      {selectedFeature.type === 'facility' && (
        <div className="space-y-2 text-xs">
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Facility Category:</span>
            <span className="text-emerald-700 font-bold uppercase">{p.facility_type}</span>
          </div>
          <div className="flex justify-between border-b border-slate-100 pb-1.5">
            <span className="text-slate-500 font-medium">Est. Capacity:</span>
            <span className="text-slate-800 font-medium">{p.capacity ? p.capacity.toLocaleString() : 'N/A'} persons</span>
          </div>
        </div>
      )}

      {/* Population & Exposure Zones Details */}
      {(selectedFeature.type === 'population_zone' || selectedFeature.type === 'population_exposure') && (
        <div className="space-y-4 font-sans text-xs">
          
          {/* Card 1: Administrative & Demographic Profile (Census 2011) */}
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 space-y-2.5">
            <div className="flex items-center justify-between border-b border-slate-200 pb-1.5">
              <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <Users className="w-3.5 h-3.5 text-blue-600" />
                <span>Census Demographics</span>
              </h4>
              <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded ${
                p.population_classification === 'HIGH' ? 'bg-blue-100 text-blue-800 border border-blue-200' :
                p.population_classification === 'MEDIUM' ? 'bg-sky-100 text-sky-800 border border-sky-200' :
                p.population_classification === 'LOW' ? 'bg-cyan-100 text-cyan-800 border border-cyan-200' :
                'bg-slate-200 text-slate-700 border border-slate-300'
              }`}>
                {p.population_classification === 'HIGH' ? 'High Population' :
                 p.population_classification === 'MEDIUM' ? 'Medium Population' :
                 p.population_classification === 'LOW' ? 'Low Population' : 'No Data'}
              </span>
            </div>

            <div className="space-y-1.5 text-[11px]">
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Administrative Area:</span>
                <span className="font-bold text-slate-900">{p.name}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Geographic Level:</span>
                <span className="font-bold text-indigo-900 bg-indigo-50 px-1.5 py-0.5 rounded border border-indigo-200 text-[10px]">
                  {p.geographic_level || p.level || 'Locality'}
                </span>
              </div>
              {p.cd_block && (
                <div className="flex justify-between border-b border-slate-100 pb-1">
                  <span className="text-slate-500 font-medium">CD Block:</span>
                  <span className="font-semibold text-slate-800">{p.cd_block}</span>
                </div>
              )}
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">District & State:</span>
                <span className="font-semibold text-slate-800">{p.district || 'Tamil Nadu'}, {p.state || 'Tamil Nadu'}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Total Population:</span>
                <span className="font-black text-slate-900 text-xs">
                  {p.population ? p.population.toLocaleString() : 'No Data'}
                </span>
              </div>
              {p.male_population !== undefined && (
                <div className="flex justify-between border-b border-slate-100 pb-1">
                  <span className="text-slate-500 font-medium">Male Population:</span>
                  <span className="font-semibold text-slate-800">{p.male_population ? p.male_population.toLocaleString() : 'N/A'}</span>
                </div>
              )}
              {p.female_population !== undefined && (
                <div className="flex justify-between border-b border-slate-100 pb-1">
                  <span className="text-slate-500 font-medium">Female Population:</span>
                  <span className="font-semibold text-slate-800">{p.female_population ? p.female_population.toLocaleString() : 'N/A'}</span>
                </div>
              )}
              {p.households !== undefined && (
                <div className="flex justify-between border-b border-slate-100 pb-1">
                  <span className="text-slate-500 font-medium">Households:</span>
                  <span className="font-semibold text-slate-800">{p.households ? p.households.toLocaleString() : 'N/A'}</span>
                </div>
              )}
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Population Density:</span>
                <span className="font-semibold text-slate-800">
                  {p.density ? `${p.density.toLocaleString()} / sq km` : (p.area_sq_km && p.population ? `${Math.round(p.population / p.area_sq_km)} / sq km` : 'Detailed Area Unavailable')}
                </span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Census Year:</span>
                <span className="font-semibold text-slate-800">{p.data_year || 'Census 2011'}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Data Source:</span>
                <span className="font-semibold text-slate-800">{p.data_source || 'Census of India'}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Boundary Status:</span>
                <span className={`font-bold px-1.5 py-0.5 rounded text-[10px] ${
                  p.boundary_status === 'Verified Administrative Boundary' 
                    ? 'text-emerald-800 bg-emerald-50 border border-emerald-200' 
                    : 'text-amber-800 bg-amber-50 border border-amber-200'
                }`}>
                  {p.boundary_status || (p.geographic_level === 'Village' || p.geographic_level === 'Town' ? 'Population boundary unavailable' : 'Verified Administrative Boundary')}
                </span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Boundary ID:</span>
                <span className="font-mono text-slate-800 text-[10px]">{p.boundary_id || p.id || 'N/A'}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Population Record ID:</span>
                <span className="font-mono text-slate-800 text-[10px]">{p.population_record_id || 'N/A'}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-1">
                <span className="text-slate-500 font-medium">Join Status:</span>
                <span className={`font-bold text-[10px] ${p.join_status?.includes('MATCHED') || p.boundary_status === 'Verified Administrative Boundary' ? 'text-emerald-700' : 'text-amber-700'}`}>
                  {p.join_status || (p.boundary_status === 'Verified Administrative Boundary' ? 'MATCHED (Administrative Polygon)' : 'NO_BOUNDARY_POLYGON')}
                </span>
              </div>
              <div className="flex justify-between items-center pt-0.5">
                <span className="text-slate-500 font-medium">Data Status:</span>
                <span className="font-bold text-amber-900 bg-amber-50 px-2 py-0.5 rounded border border-amber-200 text-[10px]">
                  {p.data_status || 'Historical Public Data'}
                </span>
              </div>
              {p.sub_district_boundary_note && (
                <div className="text-[10px] text-amber-900 bg-amber-50/80 p-2 rounded border border-amber-200 mt-1">
                  <strong>Boundary Fidelity: </strong>{p.sub_district_boundary_note}
                </div>
              )}
            </div>
          </div>

          {/* Card 2: Waterlogging Risk & Estimated Population Exposure (SEPARATELY DISPLAYED) */}
          <div className="bg-amber-50/70 border border-amber-200 rounded-lg p-3 space-y-2">
            <div className="flex items-center justify-between border-b border-amber-200/80 pb-1.5">
              <h4 className="font-bold text-amber-950 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-700" />
                <span>Waterlogging Risk & Exposure</span>
              </h4>
              <span className={`text-[10px] font-black px-2 py-0.5 rounded uppercase ${
                p.risk_level === 'HIGH' || p.risk_level === 'CRITICAL' ? 'bg-red-600 text-white' :
                p.risk_level === 'MEDIUM' ? 'bg-amber-500 text-white' :
                p.risk_level === 'LOW' ? 'bg-emerald-600 text-white' :
                'bg-slate-400 text-white'
              }`}>
                {p.risk_level || 'LOW'} RISK
              </span>
            </div>

            <div className="space-y-2 text-[11px]">
              <div className="flex justify-between items-baseline border-b border-amber-100 pb-1">
                <span className="text-slate-600 font-medium">Total Population (Demographics):</span>
                <span className="font-bold text-slate-800">{p.population ? p.population.toLocaleString() : 'No Data'}</span>
              </div>

              <div className="flex justify-between items-baseline border-b border-amber-100 pb-1">
                <span className="text-slate-700 font-bold">Estimated Exposed Population:</span>
                <span className="font-black text-red-700 text-xs">
                  {p.exposed_population ? `~${p.exposed_population.toLocaleString()} persons` : (p.population ? 'Minimal / Not in Flood Zone' : 'No Data')}
                </span>
              </div>

              {p.exposed_population_ratio && (
                <div className="text-[10px] text-amber-900 bg-white/80 p-1.5 rounded border border-amber-200">
                  <strong>Exposure Model: </strong>{p.exposed_population_ratio}
                </div>
              )}

              {p.risk_level === 'HIGH' || p.risk_level === 'CRITICAL' ? (
                <div className="text-red-700 font-bold bg-red-50 border border-red-200 p-2 rounded-lg flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-red-600 shrink-0" />
                  <span>Higher Population Exposure Signal</span>
                </div>
              ) : null}

              <p className="text-[9px] text-slate-500 italic leading-tight pt-1">
                * Note: Total Population is the demographic census count. Exposed Population represents the subset estimated to be in proximity to predicted waterlogging or stressed drainage.
              </p>
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
