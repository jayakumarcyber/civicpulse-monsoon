'use client';

import { useState, useEffect } from 'react';
import { Cpu, DollarSign, Clock, Users, CheckCircle, AlertTriangle, Sparkles } from 'lucide-react';

interface ResourcePlannerProps {
  apiBaseUrl: string;
}

export default function ResourcePlannerPanel({ apiBaseUrl }: ResourcePlannerProps) {
  const [budget, setBudget] = useState<number>(50000);
  const [hours, setHours] = useState<number>(24);
  const [teamsCount, setTeamsCount] = useState<number>(3);
  const [optimizationResult, setOptimizationResult] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const runOptimization = () => {
    setLoading(true);
    fetch(`${apiBaseUrl}/api/v1/optimization/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        available_budget: budget,
        available_hours: hours,
        available_teams_count: teamsCount,
      }),
    })
      .then((res) => res.json())
      .then((data) => setOptimizationResult(data))
      .catch((err) => console.error('Failed to run OR-Tools optimization:', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    runOptimization();
  }, [apiBaseUrl]);

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4 font-sans text-xs">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-indigo-700" />
          <div>
            <h3 className="font-bold text-slate-900 text-sm">Crew & Budget Optimization Engine</h3>
            <p className="text-[11px] text-slate-500">Constraint-satisfaction knapsack solver powered by Google OR-Tools MILP optimization framework.</p>
          </div>
        </div>
        <span className="text-[11px] font-bold text-indigo-800 bg-indigo-50 border border-indigo-200 px-3 py-1 rounded-md flex items-center space-x-1.5">
          <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
          <span>Google OR-Tools MILP Solver</span>
        </span>
      </div>

      {/* Resource Constraint Controls */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-50 border border-slate-200 p-4 rounded-lg">
        
        {/* Available Budget Slider */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-slate-700">
            <span className="flex items-center space-x-1 font-semibold">
              <DollarSign className="w-4 h-4 text-emerald-600" />
              <span>Available Budget (₹)</span>
            </span>
            <span className="font-bold text-emerald-700 text-xs">₹{budget.toLocaleString()}</span>
          </div>
          <input
            type="range"
            min="5000"
            max="100000"
            step="5000"
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
          />
        </div>

        {/* Working Hours */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-slate-700">
            <span className="flex items-center space-x-1 font-semibold">
              <Clock className="w-4 h-4 text-blue-600" />
              <span>Available Time Window</span>
            </span>
            <span className="font-bold text-blue-700 text-xs">{hours} hrs</span>
          </div>
          <input
            type="range"
            min="6"
            max="48"
            step="6"
            value={hours}
            onChange={(e) => setHours(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
          />
        </div>

        {/* Available Maintenance Teams */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-slate-700">
            <span className="flex items-center space-x-1 font-semibold">
              <Users className="w-4 h-4 text-purple-600" />
              <span>Available Crews</span>
            </span>
            <span className="font-bold text-purple-700 text-xs">{teamsCount} Crews</span>
          </div>
          <input
            type="range"
            min="1"
            max="5"
            step="1"
            value={teamsCount}
            onChange={(e) => setTeamsCount(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
          />
        </div>

      </div>

      <div className="flex justify-end">
        <button
          onClick={runOptimization}
          disabled={loading}
          className="bg-indigo-700 hover:bg-indigo-800 text-white font-semibold px-4 py-2 rounded-lg flex items-center space-x-2 text-xs transition shadow-sm disabled:opacity-50"
        >
          <Cpu className="w-4 h-4" />
          <span>{loading ? 'Solving MILP Knapsack...' : 'OPTIMIZE PLAN'}</span>
        </button>
      </div>

      {/* Infeasibility Alert Banner */}
      {optimizationResult?.optimization_status === 'NO_FEASIBLE_PLAN' && (
        <div className="bg-red-50 border border-red-200 text-red-800 p-3.5 rounded-lg flex items-start space-x-3 text-xs">
          <AlertTriangle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-xs">No Feasible Plan Under Current Constraints</h4>
            <p className="text-[11px] text-red-700 pt-0.5">{optimizationResult.infeasibility_reason}</p>
          </div>
        </div>
      )}

      {/* Optimization Results View */}
      {optimizationResult && optimizationResult.optimization_status !== 'NO_FEASIBLE_PLAN' && (
        <div className="space-y-4 pt-1">
          
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div className="bg-slate-50 border border-slate-200 p-3 rounded-lg">
              <span className="text-slate-500 text-[10px] uppercase font-bold block">Baseline Unplanned Benefit</span>
              <span className="font-bold text-slate-800 text-sm">
                {optimizationResult.comparison?.unplanned_baseline_benefit || 0} pts
              </span>
            </div>

            <div className="bg-indigo-50 border border-indigo-200 p-3 rounded-lg">
              <span className="text-indigo-800 text-[10px] uppercase font-bold block">OR-Tools Optimized Benefit</span>
              <span className="font-bold text-indigo-900 text-sm">
                {optimizationResult.comparison?.optimized_plan_benefit || 0} pts
              </span>
            </div>

            <div className="bg-emerald-50 border border-emerald-200 p-3 rounded-lg">
              <span className="text-emerald-800 text-[10px] uppercase font-bold block">Optimized Resource Usage</span>
              <span className="font-bold text-emerald-900 text-xs">
                ₹{optimizationResult.used_budget_inr?.toLocaleString()} used ({optimizationResult.used_teams_count} Crews)
              </span>
            </div>
          </div>

          {/* Recommended Interventions List */}
          <div className="space-y-2">
            <h4 className="text-[11px] font-bold uppercase tracking-wider text-slate-700">
              Recommended Crew Assignment & Intervention Sequence ({optimizationResult.selected_actions_count || 0} Actions Selected)
            </h4>

            <div className="space-y-2">
              {optimizationResult.selected_actions?.map((act: any) => (
                <div key={act.action_id} className="bg-slate-50 border border-slate-200 p-3 rounded-lg space-y-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                      <span className="font-bold text-slate-900 text-xs">{act.name}</span>
                      <span className="text-[10px] bg-slate-200 px-2 py-0.5 rounded font-bold text-slate-700">
                        {act.priority_level}
                      </span>
                    </div>
                    <span className="font-bold text-emerald-700 text-xs">₹{act.estimated_cost_inr?.toLocaleString()}</span>
                  </div>

                  <div className="flex justify-between text-[11px] text-slate-600 pt-1">
                    <span>Assigned: <strong className="text-purple-700 font-semibold">{act.assigned_team_name}</strong></span>
                    <span>Est. Duration: <strong className="text-slate-800">{act.estimated_duration_hours} hrs</strong></span>
                    <span>Expected Benefit: <strong className="text-blue-700">+{act.expected_benefit} pts</strong></span>
                  </div>

                  <p className="text-[11px] text-slate-500 pt-1 border-t border-slate-200 italic">
                    {act.recommendation_reason}
                  </p>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
