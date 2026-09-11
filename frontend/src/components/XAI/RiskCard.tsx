'use client';

import { useState, useEffect } from 'react';
import { AlertTriangle, Flame, Info } from 'lucide-react';

interface RiskCardProps {
  wardId: number;
  wardName: string;
  horizonHours?: number;
  apiBaseUrl: string;
}

export default function RiskCard({ wardId, wardName, horizonHours = 24, apiBaseUrl }: RiskCardProps) {
  const [explanationData, setExplanationData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetch(`${apiBaseUrl}/api/v1/explanations/ward/${wardId}?horizon_hours=${horizonHours}`)
      .then((res) => res.json())
      .then((data) => setExplanationData(data))
      .catch((err) => console.error('Failed to fetch explanation:', err))
      .finally(() => setLoading(false));
  }, [wardId, horizonHours, apiBaseUrl]);

  if (loading) {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-center text-xs space-y-2 text-slate-500 font-sans">
        <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p>Computing predicted waterlogging risk explanations...</p>
      </div>
    );
  }

  if (!explanationData) return null;

  const { prediction_summary, top_contributing_factors, data_quality_warnings } = explanationData;
  const probPercent = Math.round((prediction_summary?.predicted_probability || 0) * 100);
  const riskLevel = (prediction_summary?.risk_level || 'NO DATA').toUpperCase();

  const isHigh = riskLevel === 'HIGH' || riskLevel === 'CRITICAL';
  const isMed = riskLevel === 'MEDIUM';
  const isLow = riskLevel === 'LOW';

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 space-y-4 font-sans text-xs shadow-sm">
      
      {/* Header & Risk Level Badge */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <div>
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">
            {horizonHours}-Hour Forecast Horizon
          </span>
          <h3 className="text-sm font-bold text-slate-900">{wardName}</h3>
        </div>
        <div className="text-right">
          <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
            isHigh
              ? 'bg-red-100 text-red-700 border border-red-300'
              : isMed
              ? 'bg-amber-100 text-amber-800 border border-amber-300'
              : isLow
              ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
              : 'bg-slate-100 text-slate-600 border border-slate-300'
          }`}>
            {isHigh ? 'HIGH RISK' : isMed ? 'MEDIUM RISK' : isLow ? 'LOW RISK' : 'NO DATA'}
          </span>
          {probPercent > 0 && (
            <p className="text-[10px] text-slate-500 mt-1">Calibrated Prob: <strong className="text-slate-900">{probPercent}%</strong></p>
          )}
        </div>
      </div>

      {/* WHY IS THIS AREA AT RISK? (SHAP / Rule Evidence) */}
      <div className="space-y-2">
        <h4 className="text-[11px] font-bold uppercase tracking-wider text-slate-800 flex items-center space-x-1.5">
          <Flame className="w-3.5 h-3.5 text-red-600" />
          <span>WHY IS THIS AREA AT RISK?</span>
        </h4>
        <div className="space-y-2">
          {top_contributing_factors.map((factor: any, i: number) => {
            const isIncrease = factor.shap_value > 0;
            const barWidth = Math.min(100, Math.max(20, Math.abs(factor.shap_value) * 300));

            return (
              <div key={i} className="bg-slate-50 border border-slate-200 rounded-lg p-2.5 space-y-1">
                <div className="flex justify-between text-[11px] font-medium">
                  <span className="text-slate-800 font-semibold">{factor.display_name}</span>
                  <span className={`font-bold ${isIncrease ? 'text-red-700' : 'text-emerald-700'}`}>
                    {isIncrease ? 'Risk Driver (+)' : 'Risk Mitigator (-)'}
                  </span>
                </div>
                {/* Progress bar */}
                <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${isIncrease ? 'bg-red-600' : 'bg-emerald-600'}`}
                    style={{ width: `${barWidth}%` }}
                  />
                </div>
                <p className="text-[10px] text-slate-600 italic pt-0.5">{factor.text_summary}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Evidence & Provenance */}
      <div className="pt-2 border-t border-slate-100 flex justify-between items-center text-[10px] text-slate-500">
        <span>Model: <strong>{prediction_summary.model_version || 'XGBoost_v1'}</strong></span>
        <span className="text-slate-600 font-semibold">{prediction_summary.data_provenance}</span>
      </div>

    </div>
  );
}
