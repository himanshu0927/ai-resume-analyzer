import React, { useEffect, useState } from 'react';
import api from '../services/api';
import type { JobRecommendation } from '../types';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const JobRecommendationsPage: React.FC = () => {
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const res = await api.get<JobRecommendation[]>('/recommendations');
        setRecommendations(res.data);
      } catch (err) {
        console.error("Error fetching recommendations", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecommendations();
  }, []);

  if (loading) return <LoadingSkeleton />;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-slate-800">Job Recommendations</h1>
        <p className="text-slate-500 text-sm max-w-xl mx-auto">
          Target role suggestions generated exclusively from candidate technical skills, languages, and project history.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4 hover:border-blue-400 transition-colors flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-bold rounded-lg border border-blue-200">
                  {rec.match_percentage}% Suitability
                </span>
                <span className="text-xs text-slate-400">Match Rank #{idx + 1}</span>
              </div>

              <h3 className="text-xl font-bold text-slate-800">{rec.role}</h3>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Recommendation Rationale</span>
                <p className="text-xs sm:text-sm text-slate-700 font-medium leading-relaxed">{rec.reason}</p>
              </div>

              <div>
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-2">Key Matching Skills</span>
                <div className="flex flex-wrap gap-1.5">
                  {rec.key_matching_skills.map((skill, sIdx) => (
                    <span key={sIdx} className="px-2.5 py-1 bg-emerald-50 text-emerald-700 font-semibold text-xs rounded-md border border-emerald-200">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <Link
                to={`/skill-gap?target_role=${encodeURIComponent(rec.role)}`}
                className="text-xs font-bold text-blue-600 hover:underline flex items-center space-x-1"
              >
                <span>Run Skill Gap Analysis</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
