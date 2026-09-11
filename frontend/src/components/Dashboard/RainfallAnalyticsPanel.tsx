'use client';

import { useState, useEffect } from 'react';
import { CloudRain, Database, Calendar, BarChart2, CheckCircle, Info } from 'lucide-react';

interface RainfallAnalyticsPanelProps {
  selectedDistrict: string;
  apiBaseUrl: string;
}

export default function RainfallAnalyticsPanel({
  selectedDistrict,
  apiBaseUrl,
}: RainfallAnalyticsPanelProps) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDistrictRainfall = async () => {
      try {
        setLoading(true);
        setError(null);
        const dist = selectedDistrict && selectedDistrict !== 'ALL' ? selectedDistrict : 'Chennai';
        const res = await fetch(`${apiBaseUrl}/api/v1/rainfall/historical/district/${encodeURIComponent(dist)}`);
        if (!res.ok) throw new Error('Failed to load historical rainfall data');
        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message || 'Error fetching rainfall');
      } finally {
        setLoading(false);
      }
    };

    fetchDistrictRainfall();
  }, [selectedDistrict, apiBaseUrl]);

  const displayDistrict = selectedDistrict && selectedDistrict !== 'ALL' ? selectedDistrict : 'Chennai';

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-4 font-sans text-xs">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-blue-50 text-blue-800 rounded-lg">
            <CloudRain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
              <span>Historical Rainfall Analytics</span>
              <span className="text-[10px] bg-slate-100 text-slate-700 font-bold px-2 py-0.5 rounded border border-slate-200 uppercase">
                Govt/Public Dataset
              </span>
            </h2>
            <p className="text-[11px] text-slate-500">
              Selected Area: <strong className="text-blue-900 font-bold">{displayDistrict} District</strong>
            </p>
          </div>
        </div>

        {/* DATA SOURCE BADGE (Requirement 4 & 13: Never label as LIVE) */}
        <div className="flex items-center space-x-1.5 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded-lg text-[10px] font-bold text-blue-900">
          <Database className="w-3.5 h-3.5 text-blue-600" />
          <span>DATA SOURCE: Historical Government/Public Dataset</span>
        </div>
      </div>

      {loading ? (
        <div className="py-6 text-center text-slate-400 font-medium animate-pulse">
          Loading district historical rainfall dataset...
        </div>
      ) : error ? (
        <div className="py-4 text-center text-amber-700 bg-amber-50 rounded-lg p-3 border border-amber-200">
          <Info className="w-4 h-4 mx-auto mb-1 text-amber-600" />
          <span>No historical records found for {displayDistrict}. (Missing data handled transparently).</span>
        </div>
      ) : data ? (
        <div className="space-y-4">
          
          {/* Key Metrics Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-slate-800">
            <div className="bg-slate-50 border border-slate-200 p-2.5 rounded-lg">
              <span className="text-[10px] font-bold text-slate-500 uppercase block">Average Rainfall</span>
              <span className="text-base font-black text-blue-900">{data.avg_rainfall_mm} <span className="text-xs font-normal text-slate-600">mm</span></span>
            </div>

            <div className="bg-slate-50 border border-slate-200 p-2.5 rounded-lg">
              <span className="text-[10px] font-bold text-slate-500 uppercase block">Max Observed</span>
              <span className="text-base font-black text-emerald-700">{data.max_rainfall_mm} <span className="text-xs font-normal text-slate-600">mm</span></span>
            </div>

            <div className="bg-slate-50 border border-slate-200 p-2.5 rounded-lg">
              <span className="text-[10px] font-bold text-slate-500 uppercase block">Total Records</span>
              <span className="text-base font-black text-slate-900">{data.total_records} <span className="text-xs font-normal text-slate-600">entries</span></span>
            </div>

            <div className="bg-slate-50 border border-slate-200 p-2.5 rounded-lg">
              <span className="text-[10px] font-bold text-slate-500 uppercase block">Datasets Used</span>
              <span className="text-xs font-bold text-blue-800 truncate block">{data.sources_used.length} CSV Files</span>
            </div>
          </div>

          {/* Historical Records & Seasonal Breakdown Table */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-slate-800 flex items-center space-x-1">
                <BarChart2 className="w-3.5 h-3.5 text-blue-600" />
                <span>Historical Rainfall Observations ({displayDistrict})</span>
              </span>
              <span className="text-[10px] text-slate-400 font-semibold">Real Uploaded CSV Data</span>
            </div>

            <div className="overflow-x-auto border border-slate-200 rounded-lg">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-100 border-b border-slate-200 text-[10px] font-bold text-slate-600 uppercase">
                    <th className="p-2">Period / Season</th>
                    <th className="p-2">Year</th>
                    <th className="p-2">Actual Rainfall (mm)</th>
                    <th className="p-2">Normal Rainfall (mm)</th>
                    <th className="p-2">Deviation (%)</th>
                    <th className="p-2">Source CSV File</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-[11px] font-medium text-slate-700">
                  {data.historical_records?.map((rec: any, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-50">
                      <td className="p-2 font-bold text-slate-900">{rec.period_or_season}</td>
                      <td className="p-2 text-slate-600">{rec.year}</td>
                      <td className="p-2 font-black text-blue-900">{rec.actual_rainfall_mm} mm</td>
                      <td className="p-2 text-slate-500">{rec.normal_rainfall_mm ? `${rec.normal_rainfall_mm} mm` : 'N/A'}</td>
                      <td className="p-2">
                        {rec.percentage_deviation !== null && rec.percentage_deviation !== undefined ? (
                          <span className={`font-bold ${rec.percentage_deviation >= 0 ? 'text-emerald-700' : 'text-amber-700'}`}>
                            {rec.percentage_deviation > 0 ? `+${rec.percentage_deviation}%` : `${rec.percentage_deviation}%`}
                          </span>
                        ) : (
                          <span className="text-slate-400">N/A</span>
                        )}
                      </td>
                      <td className="p-2 text-[10px] text-slate-500 font-mono truncate max-w-[180px]">
                        {rec.source_file}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      ) : null}

    </div>
  );
}
