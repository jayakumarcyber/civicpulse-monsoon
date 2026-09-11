'use client';

import { useState, useEffect } from 'react';
import { Network, ArrowDown, ShieldAlert, Waves, MapPin, CheckCircle2, AlertTriangle, Layers } from 'lucide-react';

interface GraphViewProps {
  wardId: number;
  apiBaseUrl: string;
}

export default function GraphViewPanel({ wardId, apiBaseUrl }: GraphViewProps) {
  const [riskChainData, setRiskChainData] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetch(`${apiBaseUrl}/api/v1/graph/risk-chain/${wardId}`)
      .then((res) => res.json())
      .then((data) => {
        setRiskChainData(data);
        if (data.risk_propagation_chain && data.risk_propagation_chain.length > 0) {
          setSelectedNode(data.risk_propagation_chain[0]);
        }
      })
      .catch((err) => console.error('Failed to fetch risk chain graph:', err))
      .finally(() => setLoading(false));
  }, [wardId, apiBaseUrl]);

  if (loading) {
    return <div className="text-xs font-mono text-slate-400 animate-pulse">Building spatial risk dependency graph...</div>;
  }

  if (!riskChainData) return null;

  const chain = riskChainData.risk_propagation_chain || [];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl space-y-5 font-mono text-xs">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Network className="w-5 h-5 text-teal-400" />
          <h3 className="font-bold text-slate-100 font-sans text-sm">Spatial Risk Propagation Chain</h3>
        </div>
        <span className="text-[10px] text-amber-400 bg-amber-950/60 border border-amber-800/60 px-2.5 py-1 rounded-md">
          INFERRED SPATIAL DEPENDENCIES
        </span>
      </div>

      {/* Dependency Score Summary */}
      <div className="bg-slate-950 border border-slate-800 rounded-xl p-3 flex justify-between items-center text-[11px]">
        <div>
          <span className="text-slate-400 block text-[10px]">Spatial Dependency Score</span>
          <span className="font-bold text-teal-300 text-sm">{riskChainData.dependency_score} / 1.0</span>
        </div>
        <div className="text-right">
          <span className="text-slate-400 block text-[10px]">Data Quality</span>
          <span className="text-slate-300 font-semibold">{riskChainData.data_provenance}</span>
        </div>
      </div>

      {/* Vertical Interactive Node Chain */}
      <div className="space-y-2">
        <h4 className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
          Dependency Chain Nodes (Click to Inspect)
        </h4>

        <div className="space-y-1.5">
          {chain.map((step: any, idx: number) => {
            const isSelected = selectedNode?.node_id === step.node_id;
            const isLast = idx === chain.length - 1;

            return (
              <div key={step.node_id} className="flex flex-col items-center">
                <button
                  onClick={() => setSelectedNode(step)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl border transition text-left ${
                    isSelected
                      ? 'bg-blue-950/80 border-blue-500 text-blue-200 shadow-lg'
                      : 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <span className="w-5 h-5 rounded-full bg-slate-800 flex items-center justify-center text-[10px] font-bold text-slate-400">
                      {idx + 1}
                    </span>
                    <div>
                      <span className="font-bold font-sans text-xs text-slate-100 block">{step.name}</span>
                      <span className="text-[10px] text-slate-400 uppercase">{step.node_type.replace('_', ' ')}</span>
                    </div>
                  </div>
                  <span className="text-[9px] bg-slate-900 border border-slate-800 px-2 py-0.5 rounded text-slate-400">
                    {step.relationship}
                  </span>
                </button>

                {!isLast && (
                  <div className="my-1 text-slate-600 flex flex-col items-center">
                    <ArrowDown className="w-4 h-4 animate-bounce text-teal-400" />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Selected Node Details Box */}
      {selectedNode && (
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-3.5 space-y-2 text-[11px]">
          <div className="flex justify-between border-b border-slate-800 pb-1.5">
            <span className="font-bold text-slate-200">{selectedNode.name}</span>
            <span className="text-teal-400 uppercase text-[10px]">{selectedNode.node_type}</span>
          </div>
          <div className="flex justify-between text-slate-400 text-[10px]">
            <span>Status: <strong className="text-slate-200">{selectedNode.status}</strong></span>
            <span>Relationship: <strong className="text-amber-400">{selectedNode.relationship}</strong></span>
          </div>
          <p className="text-[10px] text-slate-400 pt-1 italic border-t border-slate-900">
            Spatial relationship inferred from PostGIS proximity thresholds. Not confirmed hydrological flow.
          </p>
        </div>
      )}

    </div>
  );
}
