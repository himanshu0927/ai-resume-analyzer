import React, { useEffect, useState } from 'react';
import api from '../services/api';
import type { SkillGapAnalysis } from '../types';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { 
  Target, 
  CheckCircle, 
  MinusCircle, 
  AlertCircle, 
  BookOpen, 
  Code2
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell, 
  Tooltip, 
  Legend 
} from 'recharts';

const TARGET_ROLES = [
  'Full Stack Developer',
  'Frontend Developer',
  'Backend Developer',
  'Python Developer',
  'Data Scientist',
  'Machine Learning Engineer',
  'Data Analyst',
  'DevOps Engineer',
  'Cloud Engineer'
];

export const SkillGapPage: React.FC = () => {
  const [selectedRole, setSelectedRole] = useState('Full Stack Developer');
  const [gapData, setGapData] = useState<SkillGapAnalysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSkillGap = async () => {
      setLoading(true);
      try {
        const res = await api.get<SkillGapAnalysis>(`/skill-gap?target_role=${encodeURIComponent(selectedRole)}`);
        setGapData(res.data);
      } catch (err) {
        console.error("Skill gap error", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSkillGap();
  }, [selectedRole]);

  const pieChartData = gapData ? [
    { name: 'Already Learned', value: gapData.stats.learned_count, color: '#10B981' },
    { name: 'Partially Covered', value: gapData.stats.partial_count, color: '#F59E0B' },
    { name: 'Missing Skills', value: gapData.stats.missing_count, color: '#EF4444' },
  ] : [];

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-800">Skill Gap Analysis</h1>
          <p className="text-slate-500 text-sm mt-1">
            Compare your detected technical profile against target role requirements to identify missing skills and roadmap learning objectives.
          </p>
        </div>

        {/* Role Selector */}
        <div className="flex items-center space-x-3 bg-white p-2 rounded-xl border border-slate-200 shadow-2xs">
          <Target className="w-5 h-5 text-blue-600 ml-2" />
          <select
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
            className="px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg text-slate-800 text-sm font-semibold focus:outline-hidden"
          >
            {TARGET_ROLES.map(role => (
              <option key={role} value={role}>{role}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <LoadingSkeleton />
      ) : gapData ? (
        <div className="space-y-8">
          {/* Top Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-emerald-50 border border-emerald-200 p-6 rounded-2xl flex items-center space-x-4">
              <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
                {gapData.stats.learned_count}
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-800">Already Learned</span>
                <p className="text-2xl font-extrabold text-emerald-900">{gapData.stats.learned_percentage}%</p>
              </div>
            </div>

            <div className="bg-amber-50 border border-amber-200 p-6 rounded-2xl flex items-center space-x-4">
              <div className="w-12 h-12 rounded-xl bg-amber-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
                {gapData.stats.partial_count}
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-amber-800">Partially Covered</span>
                <p className="text-2xl font-extrabold text-amber-900">{gapData.stats.partial_percentage}%</p>
              </div>
            </div>

            <div className="bg-red-50 border border-red-200 p-6 rounded-2xl flex items-center space-x-4">
              <div className="w-12 h-12 rounded-xl bg-red-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
                {gapData.stats.missing_count}
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-red-800">Missing Skills</span>
                <p className="text-2xl font-extrabold text-red-900">{gapData.stats.missing_percentage}%</p>
              </div>
            </div>
          </div>

          {/* Chart & Skill Comparison Lists */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Visual Skill-Gap Chart */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex flex-col items-center justify-center space-y-4 lg:col-span-1">
              <h3 className="text-base font-bold text-slate-800 self-start">Target Skill Alignment</h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pieChartData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {pieChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend verticalAlign="bottom" height={36} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Categorized Lists */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs lg:col-span-2 space-y-6">
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-1.5">
                  <CheckCircle className="w-4 h-4 text-emerald-500" />
                  <span>Already Learned Skills ({gapData.already_learned.length})</span>
                </h4>
                <div className="flex flex-wrap gap-2">
                  {gapData.already_learned.map((s, idx) => (
                    <span key={idx} className="px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-lg border border-emerald-200">
                      {s}
                    </span>
                  ))}
                  {gapData.already_learned.length === 0 && <span className="text-xs text-slate-400">None detected yet.</span>}
                </div>
              </div>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-1.5">
                  <MinusCircle className="w-4 h-4 text-amber-500" />
                  <span>Partially Covered Skills ({gapData.partially_covered.length})</span>
                </h4>
                <div className="flex flex-wrap gap-2">
                  {gapData.partially_covered.map((s, idx) => (
                    <span key={idx} className="px-3 py-1 bg-amber-50 text-amber-700 text-xs font-semibold rounded-lg border border-amber-200">
                      ~ {s}
                    </span>
                  ))}
                  {gapData.partially_covered.length === 0 && <span className="text-xs text-slate-400">None</span>}
                </div>
              </div>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-1.5">
                  <AlertCircle className="w-4 h-4 text-red-500" />
                  <span>Missing Skills ({gapData.missing.length})</span>
                </h4>
                <div className="flex flex-wrap gap-2">
                  {gapData.missing.map((s, idx) => (
                    <span key={idx} className="px-3 py-1 bg-red-50 text-red-700 text-xs font-semibold rounded-lg border border-red-200">
                      + {s}
                    </span>
                  ))}
                  {gapData.missing.length === 0 && <span className="text-xs text-emerald-600 font-semibold">Full skill coverage achieved!</span>}
                </div>
              </div>
            </div>
          </div>

          {/* Learning Suggestions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
                <BookOpen className="w-5 h-5 text-blue-600" />
                <span>Topics to Learn & Master</span>
              </h3>
              <ul className="space-y-2 text-xs sm:text-sm text-slate-700">
                {gapData.learning_suggestions.topics_to_learn.map((t, idx) => (
                  <li key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-center space-x-2">
                    <span className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0"></span>
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
                <Code2 className="w-5 h-5 text-purple-600" />
                <span>Suggested Portfolio Project Ideas</span>
              </h3>
              <ul className="space-y-2 text-xs sm:text-sm text-slate-700">
                {gapData.learning_suggestions.suggested_project_ideas.map((p, idx) => (
                  <li key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p className="font-semibold text-slate-800">{p}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
