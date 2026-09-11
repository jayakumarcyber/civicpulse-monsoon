'use client';

import { useState } from 'react';
import { Search, MapPin, Building2, Globe, Flag } from 'lucide-react';

interface SearchBarProps {
  geoData: {
    wards: any;
    roads: any;
    drains: any;
    facilities: any;
    incidents: any;
    districts?: any;
    state?: any;
  };
  onSelectSearchResult: (feature: any) => void;
  apiBaseUrl?: string;
  selectedDistrict?: string;
}

const REGIONAL_LOCATIONS = [
  { name: 'India', type: 'country', coordinates: [78.9629, 20.5937], level: 5 },
  { name: 'Tamil Nadu', type: 'state', coordinates: [78.6569, 11.1271], level: 7.5 },
  { name: 'Chennai District', city: 'Chennai', type: 'district', coordinates: [80.2707, 13.0827], level: 11 },
  { name: 'Coimbatore District', city: 'Coimbatore', type: 'district', coordinates: [76.9558, 11.0168], level: 11 },
  { name: 'Salem District', city: 'Salem', type: 'district', coordinates: [78.1460, 11.6643], level: 11 },
  { name: 'Madurai District', city: 'Madurai', type: 'district', coordinates: [78.1198, 9.9252], level: 11 },
  { name: 'Tiruchirappalli District', city: 'Tiruchirappalli', type: 'district', coordinates: [78.7047, 10.7905], level: 11 },
  { name: 'Tiruppur District', city: 'Tiruppur', type: 'district', coordinates: [77.3411, 11.1085], level: 11 },
  { name: 'Erode District', city: 'Erode', type: 'district', coordinates: [77.7172, 11.3410], level: 11 },
  { name: 'Vellore District', city: 'Vellore', type: 'district', coordinates: [79.1325, 12.9165], level: 11 },
  { name: 'Tirunelveli District', city: 'Tirunelveli', type: 'district', coordinates: [77.7567, 8.7139], level: 11 },
  { name: 'Kanchipuram District', city: 'Kanchipuram', type: 'district', coordinates: [79.7036, 12.8342], level: 11 },
  { name: 'Kallakurichi District', city: 'Kallakurichi', type: 'district', coordinates: [78.9620, 11.7380], level: 11 },
  { name: 'Villupuram District', city: 'Villupuram', type: 'district', coordinates: [79.4920, 11.9400], level: 11 },
  { name: 'Mumbai', city: 'Mumbai', type: 'city', coordinates: [72.8777, 19.0760], level: 11 },
];

export default function SearchBar({
  geoData,
  onSelectSearchResult,
  apiBaseUrl = 'http://localhost:8000',
  selectedDistrict = 'ALL'
}: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async (text: string) => {
    setQuery(text);
    if (!text.trim() || text.length < 2) {
      setResults([]);
      return;
    }

    try {
      // Query dynamic geocoding endpoint
      const url = `${apiBaseUrl}/api/v1/search?q=${encodeURIComponent(text)}&district=${selectedDistrict}`;
      const response = await fetch(url);
      if (response.ok) {
        const matches = await response.json();
        if (matches && matches.length > 0) {
          setResults(matches.slice(0, 8));
          return;
        }
      }
    } catch (err) {
      console.error("[SEARCH] Geocoding API failed, falling back to local:", err);
    }

    // Fallback: Local offline client-side search
    const term = text.toLowerCase();
    const matches: any[] = [];

    REGIONAL_LOCATIONS.forEach((loc) => {
      if (loc.name.toLowerCase().includes(term) || (loc.city && loc.city.toLowerCase().includes(term))) {
        if (selectedDistrict === 'ALL' || !loc.city || loc.city.toLowerCase() === selectedDistrict.toLowerCase()) {
          matches.push({
            label: `${loc.type === 'country' ? '🇮🇳 ' : loc.type === 'state' ? 'State: ' : 'District: '}${loc.name}`,
            type: loc.type,
            feature: {
              id: `loc-${loc.name}`,
              type: 'Feature',
              geometry: { type: 'Point', coordinates: loc.coordinates },
              properties: { name: loc.name, city: loc.city || loc.name, type: loc.type, level: loc.level },
            },
          });
        }
      }
    });

    if (geoData.wards?.features) {
      geoData.wards.features.forEach((f: any) => {
        const name = f.properties?.name || '';
        const city = f.properties?.city || f.properties?.district || '';
        const code = f.properties?.ward_code || '';
        if (name.toLowerCase().includes(term) || city.toLowerCase().includes(term) || code.toLowerCase().includes(term)) {
          matches.push({
            label: `Ward: ${name} (${city})`,
            type: 'ward',
            feature: f,
          });
        }
      });
    }

    setResults(matches.slice(0, 8));
  };

  const handleSelect = (item: any) => {
    setQuery(item.label);
    setResults([]);
    onSelectSearchResult(item.feature);
  };

  return (
    <div className="relative w-full max-w-sm">
      <div className="relative flex items-center">
        <Search className="w-4 h-4 absolute left-3 text-slate-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="Search India, Tamil Nadu, Chennai, Salem..."
          className="w-full bg-white border border-slate-300 rounded-lg pl-9 pr-4 py-2 text-xs font-medium text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 shadow-sm"
        />
      </div>

      {results.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-lg shadow-lg overflow-hidden z-50 text-xs">
          {results.map((r, i) => (
            <button
              key={i}
              onClick={() => handleSelect(r)}
              className="w-full text-left px-3 py-2.5 hover:bg-slate-50 flex items-center space-x-2 text-slate-700 border-b border-slate-100 last:border-none"
            >
              {r.type === 'country' || r.type === 'state' ? (
                <Globe className="w-4 h-4 text-blue-600 shrink-0" />
              ) : r.type === 'district' ? (
                <Building2 className="w-4 h-4 text-amber-600 shrink-0" />
              ) : (
                <MapPin className="w-4 h-4 text-slate-500 shrink-0" />
              )}
              <span className="truncate font-medium">{r.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
