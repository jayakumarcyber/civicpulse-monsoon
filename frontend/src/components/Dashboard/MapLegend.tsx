'use client';

export default function MapLegend() {
  return (
    <div className="bg-white/95 border border-slate-300 rounded-lg p-3 shadow-md backdrop-blur-sm text-[11px] font-sans space-y-2 max-w-xs text-slate-800">
      <div className="font-bold text-slate-700 uppercase tracking-wider text-[10px] border-b border-slate-200 pb-1">
        Risk & GIS Map Legend
      </div>
      
      {/* 1. Risk Level Semantics */}
      <div className="space-y-1 py-1 border-b border-slate-100">
        <div className="text-[10px] font-semibold text-slate-500 uppercase">Predicted Risk Level</div>
        <div className="grid grid-cols-2 gap-x-3 gap-y-1">
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-red-600 border border-red-700 shrink-0" />
            <span className="font-semibold text-red-700">HIGH RISK</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-amber-500 border border-amber-600 shrink-0" />
            <span className="font-semibold text-amber-800">MEDIUM RISK</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-emerald-500 border border-emerald-600 shrink-0" />
            <span className="font-semibold text-emerald-800">LOW RISK</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-slate-400 border border-slate-500 shrink-0" />
            <span className="font-semibold text-slate-600">NO DATA</span>
          </div>
        </div>
      </div>

      {/* 2. Population Zones (Demographics) */}
      <div className="space-y-1 py-1 border-b border-slate-100">
        <div className="text-[10px] font-semibold text-slate-500 uppercase">Population Choropleth (Census 2011)</div>
        <div className="grid grid-cols-2 gap-x-3 gap-y-1">
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-blue-700 border border-blue-800 shrink-0" />
            <span className="font-semibold text-blue-900 text-[10px]">High Population</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-sky-500 border border-sky-600 shrink-0" />
            <span className="font-semibold text-sky-800 text-[10px]">Medium Population</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-cyan-400 border border-cyan-500 shrink-0" />
            <span className="font-semibold text-cyan-800 text-[10px]">Low Population</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-sm bg-slate-200 border border-dashed border-slate-400 shrink-0" />
            <span className="font-semibold text-slate-600 text-[10px]">No Data</span>
          </div>
        </div>
      </div>

      {/* 3. Feature Symbology */}
      <div className="grid grid-cols-2 gap-x-3 gap-y-1 pt-0.5">
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-red-600 inline-block border border-white shrink-0" />
          <span className="text-slate-600 text-[10px]">Incident</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-0.5 bg-red-600 inline-block shrink-0" />
          <span className="text-slate-600 text-[10px]">Choked Drain</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 inline-block border border-white shrink-0" />
          <span className="text-slate-600 text-[10px]">Hospital</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-purple-600 inline-block border border-white shrink-0" />
          <span className="text-slate-600 text-[10px]">School</span>
        </div>
      </div>
    </div>
  );
}
