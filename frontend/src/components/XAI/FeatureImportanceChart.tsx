'use client';

import { useState, useEffect } from 'react';
import { BarChart3, Layers } from 'lucide-react';

interface FeatureImportanceProps {
  apiBaseUrl: string;
}

export default function FeatureImportanceChart({ apiBaseUrl }: FeatureImportanceProps) {
  const [importanceList, setImportanceList] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch(`${apiBaseUrl}/api/v1/explanations/model/feature-importance?horizon_hours=24`)
      .then((res) => res.json())
      .then((data) => setImportanceList(data))
      .catch((err) => console.error('Failed to fetch feature importance:', err))
      .finally(() => setLoading(false));
  }, [apiBaseUrl]);

  if (loading) {
    return <div className="text-xs text-slate-500 font-mono animate-pulse">Loading global SHAP feature importances...</div>;
  }

  const maxScore = importanceList.length > 0 ? Math.max(...importanceList.map((x) => x.global_importance_score)) : 1.0;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4 font-mono text-xs">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="font-bold text-slate-200 font-sans flex items-center space-x-2">
          <BarChart3 className="w-4 h-4 text-purple-400" />
          <span>Global SHAP Feature Importance Ranking</span>
        </h3>
        <span className="text-[10px] text-slate-500 uppercase">24-Hour Horizon Model</span>
      </div>

      <div className="space-y-2">
        {importanceList.slice(0, 8).map((item, idx) => {
          const widthPct = Math.min(100, Math.max(10, (item.global_importance_score / maxScore) * 100));
          return (
            <div key={idx} className="space-y-1 text-[11px]">
              <div className="flex justify-between text-[10px]">
                <span className="text-slate-300 font-semibold">{item.display_name}</span>
                <span className="text-purple-300 font-bold">{item.global_importance_score}</span>
              </div>
              <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                  style={{ width: `${widthPct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
