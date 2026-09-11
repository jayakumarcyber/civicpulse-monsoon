'use client';

import { Filter, Layers, Eye, EyeOff, Globe, MapPin, Compass, Navigation, Building2, Trees } from 'lucide-react';

interface FilterPanelProps {
  layers: {
    wards: boolean;
    roads: boolean;
    drains: boolean;
    waterbodies: boolean;
    incidents: boolean;
    facilities: boolean;
    population: boolean;
    districts?: boolean;
    state?: boolean;
  };
  onToggleLayer: (layerName: string) => void;
  filters: {
    stateId: string;
    districtId: string;
    adminType: string;
    localBody: string;
    wardId: string;
    incidentType: string;
    severity: string;
    facilityType: string;
  };
  onFilterChange: (key: string, value: string) => void;
  wardsList: Array<{ id: number; name: string; district?: string; local_body?: string; administrative_type?: string }>;
  onFocusCamera: (type: 'india' | 'tn' | 'district' | 'ward') => void;
}

export const ALL_38_TN_DISTRICTS = [
  "Ariyalur",
  "Chengalpattu",
  "Chennai",
  "Coimbatore",
  "Cuddalore",
  "Dharmapuri",
  "Dindigul",
  "Erode",
  "Kallakurichi",
  "Kancheepuram",
  "Karur",
  "Krishnagiri",
  "Madurai",
  "Mayiladuthurai",
  "Nagapattinam",
  "Kanniyakumari",
  "Namakkal",
  "Perambalur",
  "Pudukkottai",
  "Ramanathapuram",
  "Ranipet",
  "Salem",
  "Sivagangai",
  "Tenkasi",
  "Thanjavur",
  "Theni",
  "Thiruvallur",
  "Thiruvarur",
  "Thoothukudi",
  "Tiruchirappalli",
  "Tirunelveli",
  "Tirupathur",
  "Tiruppur",
  "Tiruvannamalai",
  "The Nilgiris",
  "Vellore",
  "Viluppuram",
  "Virudhunagar"
];

// District-Specific Urban Local Bodies & Taluks Dictionary
const DISTRICT_LOCAL_BODIES: Record<string, { urban: string[]; rural: string[] }> = {
  "Chennai": {
    urban: ["Greater Chennai Corporation (Zones 1-15)"],
    rural: []
  },
  "Coimbatore": {
    urban: ["Coimbatore City Municipal Corporation", "Mettupalayam Municipality", "Pollachi Municipality"],
    rural: ["Pollachi Taluk", "Mettupalayam Block", "Sulur Block"]
  },
  "Salem": {
    urban: ["Salem City Municipal Corporation", "Attur Municipality", "Mettur Municipality"],
    rural: ["Salem Taluk", "Attur Block", "Omalur Block"]
  },
  "Madurai": {
    urban: ["Madurai City Municipal Corporation", "Melur Municipality", "Thirumangalam Municipality"],
    rural: ["Madurai East Taluk", "Melur Block", "Usilampatti Block"]
  },
  "Kallakurichi": {
    urban: ["Kallakurichi Municipality", "Tirukkoyilur Municipality"],
    rural: ["Kallakurichi Taluk", "Tirukkoyilur Block", "Sankarapuram Block", "Rishivandiyam Panchayat"]
  },
  "Ariyalur": {
    urban: ["Ariyalur Municipality", "Jayamkondam Municipality"],
    rural: ["Ariyalur Taluk", "Sendurai Block", "Udayarpalayam Block"]
  },
  "Chengalpattu": {
    urban: ["Tambaram City Municipal Corporation", "Chengalpattu Municipality"],
    rural: ["Chengalpattu Taluk", "Thiruporur Block", "Kattankulathur Block"]
  },
  "Cuddalore": {
    urban: ["Cuddalore City Corporation", "Panruti Municipality", "Chidambaram Municipality"],
    rural: ["Cuddalore Taluk", "Kurinjipadi Block", "Chidambaram Block"]
  },
  "Tiruchirappalli": {
    urban: ["Tiruchirappalli City Municipal Corporation", "Manapparai Municipality", "Thuvakudi Municipality"],
    rural: ["Srirangam Taluk", "Lalgudi Block", "Thottiyam Block"]
  },
  "Tirunelveli": {
    urban: ["Tirunelveli City Municipal Corporation", "Ambasamudram Municipality"],
    rural: ["Tirunelveli Taluk", "Cheranmahadevi Block", "Nanguneri Block"]
  }
};

export default function FilterPanel({
  layers,
  onToggleLayer,
  filters,
  onFilterChange,
  wardsList,
  onFocusCamera,
}: FilterPanelProps) {

  // Filter Wards List by selected District & Admin Type
  const filteredWards = wardsList.filter((w) => {
    if (filters.districtId !== 'ALL' && w.district && w.district.toLowerCase() !== filters.districtId.toLowerCase()) {
      return false;
    }
    if (filters.adminType !== 'ALL' && w.administrative_type && w.administrative_type.toLowerCase() !== filters.adminType.toLowerCase()) {
      return false;
    }
    return true;
  });

  const availableLocalBodies = filters.districtId !== 'ALL' && DISTRICT_LOCAL_BODIES[filters.districtId]
    ? (filters.adminType === 'Rural' ? DISTRICT_LOCAL_BODIES[filters.districtId].rural : DISTRICT_LOCAL_BODIES[filters.districtId].urban)
    : [];

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 space-y-4 shadow-sm text-xs font-sans">
      
      {/* 1. Quick Navigation Focus Controls */}
      <div>
        <h3 className="font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5 text-[11px]">
          <Compass className="w-4 h-4 text-blue-600" />
          <span>Quick Map View Focus</span>
        </h3>

        <div className="grid grid-cols-2 gap-2 text-[11px]">
          <button
            onClick={() => onFocusCamera('india')}
            className="w-full bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold py-1.5 px-2 rounded-lg border border-slate-300 transition flex items-center justify-center space-x-1"
          >
            <span>🇮🇳 Focus India</span>
          </button>

          <button
            onClick={() => onFocusCamera('tn')}
            className="w-full bg-blue-50 hover:bg-blue-100 text-blue-900 font-semibold py-1.5 px-2 rounded-lg border border-blue-200 transition flex items-center justify-center space-x-1"
          >
            <span>Focus Tamil Nadu</span>
          </button>

          <button
            onClick={() => onFocusCamera('district')}
            className="w-full bg-amber-50 hover:bg-amber-100 text-amber-900 font-semibold py-1.5 px-2 rounded-lg border border-amber-200 transition flex items-center justify-center space-x-1"
          >
            <span>Focus District</span>
          </button>

          <button
            onClick={() => onFocusCamera('ward')}
            className="w-full bg-emerald-50 hover:bg-emerald-100 text-emerald-900 font-semibold py-1.5 px-2 rounded-lg border border-emerald-200 transition flex items-center justify-center space-x-1"
          >
            <span>Focus Ward</span>
          </button>
        </div>
      </div>

      <hr className="border-slate-200" />

      {/* 2. Cascading Administrative Hierarchy Selection (Requirements 1, 3, 5, 6, 12) */}
      <div>
        <h3 className="font-bold uppercase tracking-wider text-slate-700 mb-2.5 flex items-center space-x-1.5 text-[11px]">
          <Navigation className="w-4 h-4 text-blue-600" />
          <span>Cascading Administrative Hierarchy</span>
        </h3>

        <div className="space-y-2.5">
          
          {/* Level 1: State */}
          <div>
            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">State</label>
            <select
              value={filters.stateId}
              onChange={(e) => onFilterChange('stateId', e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-800 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Tamil Nadu">Tamil Nadu (38 Districts Focus)</option>
              <option value="ALL">All India States</option>
            </select>
          </div>

          {/* Level 2: District (All 38 Official TN Districts) */}
          <div>
            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1 flex items-center justify-between">
              <span>District (38 TN Districts)</span>
              {filters.districtId !== 'ALL' && <span className="text-[9px] text-blue-700 font-extrabold uppercase">Selected</span>}
            </label>
            <select
              value={filters.districtId}
              onChange={(e) => {
                onFilterChange('districtId', e.target.value);
                onFilterChange('wardId', 'ALL');
                onFilterChange('localBody', 'ALL');
                if (e.target.value !== 'ALL') onFocusCamera('district');
              }}
              className="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-800 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">All Districts (Tamil Nadu)</option>
              {ALL_38_TN_DISTRICTS.map((d, i) => (
                <option key={d} value={d}>{i + 1}. {d} District</option>
              ))}
            </select>
          </div>

          {/* Level 3: Administrative Type (Urban vs Rural) */}
          <div>
            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Administrative Type</label>
            <div className="grid grid-cols-3 gap-1 text-[10px]">
              {[
                { id: 'ALL', label: 'All Types' },
                { id: 'Urban', label: 'Urban (ULB)' },
                { id: 'Rural', label: 'Rural' },
              ].map((t) => (
                <button
                  key={t.id}
                  onClick={() => {
                    onFilterChange('adminType', t.id);
                    onFilterChange('localBody', 'ALL');
                  }}
                  className={`py-1 px-1.5 rounded text-center font-bold border transition ${
                    filters.adminType === t.id
                      ? 'bg-blue-900 text-white border-blue-900'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          {/* Level 4: Local Body / Taluk / Block */}
          {availableLocalBodies.length > 0 && (
            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">
                {filters.adminType === 'Rural' ? 'Taluk / Panchayat Block' : 'Corporation / Municipality'}
              </label>
              <select
                value={filters.localBody}
                onChange={(e) => onFilterChange('localBody', e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-800 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="ALL">All Local Bodies / Taluks</option>
                {availableLocalBodies.map((lb) => (
                  <option key={lb} value={lb}>{lb}</option>
                ))}
              </select>
            </div>
          )}

          {/* Level 5: Ward / Village / Locality Selection */}
          <div>
            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">
              {filters.adminType === 'Rural' ? 'Village / Habitation' : 'Ward Number / Locality'}
            </label>
            <select
              value={filters.wardId}
              onChange={(e) => {
                onFilterChange('wardId', e.target.value);
                if (e.target.value !== 'ALL') onFocusCamera('ward');
              }}
              className="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-800 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">
                {filters.districtId !== 'ALL' ? `All Wards (${filters.districtId})` : 'All Wards (Tamil Nadu)'}
              </option>
              {filteredWards.map((w) => (
                <option key={w.id} value={w.id}>{w.name}</option>
              ))}
            </select>
          </div>

        </div>
      </div>

      <hr className="border-slate-200" />

      {/* 3. Layer Visibility Controls */}
      <div>
        <h3 className="font-bold uppercase tracking-wider text-slate-700 mb-2.5 flex items-center space-x-1.5 text-[11px]">
          <Layers className="w-4 h-4 text-blue-600" />
          <span>Geographic Layer Controls</span>
        </h3>
        <div className="space-y-1.5">
          {[
            { key: 'districts', label: '38 TN District Boundaries', color: 'bg-amber-500' },
            { key: 'wards', label: 'Wards & Localities (Risk Layer)', color: 'bg-red-500' },
            { key: 'population', label: 'Population & Exposure Zones', color: 'bg-blue-600' },
            { key: 'roads', label: 'Road Network', color: 'bg-orange-500' },
            { key: 'drains', label: 'Drainage Outfalls', color: 'bg-sky-500' },
            { key: 'waterbodies', label: 'Rivers & Waterbodies', color: 'bg-blue-700' },
            { key: 'incidents', label: 'Waterlogging Incidents', color: 'bg-red-600' },
            { key: 'facilities', label: 'Facilities & POIs (Hospitals, Schools)', color: 'bg-emerald-500' },
          ].map((item) => {
            const active = (layers as any)[item.key];
            return (
              <button
                key={item.key}
                onClick={() => onToggleLayer(item.key)}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg transition border text-xs font-medium ${
                  active
                    ? 'bg-slate-100 border-slate-300 text-slate-900'
                    : 'bg-slate-50 border-slate-100 text-slate-400 hover:text-slate-600'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className={`w-2.5 h-2.5 rounded-full ${item.color}`} />
                  <span className="truncate">{item.label}</span>
                </div>
                {active ? <Eye className="w-3.5 h-3.5 text-blue-600 shrink-0" /> : <EyeOff className="w-3.5 h-3.5 text-slate-400 shrink-0" />}
              </button>
            );
          })}
        </div>
      </div>

    </div>
  );
}
