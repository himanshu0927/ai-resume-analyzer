import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import type { Resume, ResumeAnalysis, JobMatch, JobRecommendation } from '../types';
import { ScoreRing } from '../components/common/ScoreRing';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { 
  FileText, 
  Award, 
  Briefcase, 
  CheckCircle, 
  AlertCircle, 
  ArrowRight, 
  Upload
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  Radar 
} from 'recharts';

export const DashboardPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [latestAnalysis, setLatestAnalysis] = useState<ResumeAnalysis | null>(null);
  const [matches, setMatches] = useState<JobMatch[]>([]);
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [resRes, matchRes, recRes] = await Promise.all([
          api.get<Resume[]>('/resumes'),
          api.get<JobMatch[]>('/job-match/history'),
          api.get<JobRecommendation[]>('/recommendations')
        ]);

        setResumes(resRes.data);
        setMatches(matchRes.data);
        setRecommendations(recRes.data);

        if (resRes.data.length > 0) {
          const latestRes = resRes.data[0];
          try {
            const anaRes = await api.get<ResumeAnalysis>(`/resumes/${latestRes.id}/analysis`);
            setLatestAnalysis(anaRes.data);
          } catch (e) {
            console.error("No analysis yet for latest resume", e);
          }
        }
      } catch (err) {
        console.error("Dashboard error:", err);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  if (loading) return <LoadingSkeleton />;

  // Prepare radar chart data from factors
  const radarData = latestAnalysis?.score_factors?.map(f => ({
    subject: f.factor.replace('Technical ', '').replace(' & Readability', ''),
    score: f.score,
    fullMark: 100
  })) || [
    { subject: 'Skills', score: 80, fullMark: 100 },
    { subject: 'Experience', score: 75, fullMark: 100 },
    { subject: 'Projects', score: 85, fullMark: 100 },
    { subject: 'Education', score: 90, fullMark: 100 },
    { subject: 'Formatting', score: 70, fullMark: 100 },
  ];

  const topSkills = latestAnalysis?.raw_extracted_data?.all_skills?.slice(0, 8) || ['Python', 'SQL', 'React', 'Git'];
  const missingSkills = matches.length > 0 ? matches[0].missing_skills.slice(0, 5) : ['Docker', 'AWS', 'Kubernetes'];

  return (
    <div className="space-y-8">
      {/* Welcome Hero Card */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 rounded-2xl p-6 md:p-8 text-white shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 border border-slate-800">
        <div className="space-y-2 max-w-2xl text-center md:text-left">
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Career Overview & Insights
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Welcome back! Upload your latest resume to benchmark skills, analyze keyword coverage, and evaluate job description matches.
          </p>
        </div>
        <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
          <Link
            to="/analyzer"
            className="px-5 py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl text-sm transition-all shadow-md shadow-blue-600/30 flex items-center justify-center space-x-2"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Resume</span>
          </Link>
          <Link
            to="/job-matcher"
            className="px-5 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl text-sm border border-slate-700 transition-colors flex items-center justify-center space-x-2"
          >
            <Briefcase className="w-4 h-4" />
            <span>Match Job</span>
          </Link>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Analyzed</p>
            <h3 className="text-2xl font-bold text-slate-800">{resumes.length}</h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center flex-shrink-0">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Latest Resume Score</p>
            <h3 className="text-2xl font-bold text-slate-800">
              {latestAnalysis ? `${latestAnalysis.overall_score}/100` : 'N/A'}
            </h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center flex-shrink-0">
            <Briefcase className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Matched Jobs</p>
            <h3 className="text-2xl font-bold text-slate-800">{matches.length}</h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center flex-shrink-0">
            <CheckCircle className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Detected Skills</p>
            <h3 className="text-2xl font-bold text-slate-800">
              {latestAnalysis?.raw_extracted_data?.total_count || 0}
            </h3>
          </div>
        </div>
      </div>

      {/* Main Insights Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Score Ring & Chart */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs lg:col-span-1 flex flex-col items-center justify-center space-y-6">
          <h3 className="text-base font-bold text-slate-800 self-start">Overall Resume Score</h3>
          {latestAnalysis ? (
            <ScoreRing score={latestAnalysis.overall_score} size={160} label="Resume Analysis Score" />
          ) : (
            <div className="py-12 text-center text-slate-400 text-sm">
              No resume analyzed yet. Upload a document to view score.
            </div>
          )}

          <div className="w-full pt-4 border-t border-slate-100">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Factor Distribution</h4>
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#e2e8f0" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10 }} />
                  <Radar name="Score" dataKey="score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.4} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Skills & Recommendations */}
        <div className="lg:col-span-2 space-y-8">
          {/* Detected & Missing Skills */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-6">
            <div>
              <h3 className="text-base font-bold text-slate-800 mb-3 flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-emerald-500" />
                <span>Top Detected Skills</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {topSkills.map((s, idx) => (
                  <span key={idx} className="px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-lg border border-emerald-200">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-base font-bold text-slate-800 mb-3 flex items-center space-x-2">
                <AlertCircle className="w-5 h-5 text-amber-500" />
                <span>Target Skill Gaps to Improve</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {missingSkills.map((s, idx) => (
                  <span key={idx} className="px-3 py-1 bg-amber-50 text-amber-700 text-xs font-semibold rounded-lg border border-amber-200">
                    + {s}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Recommended Job Roles */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-slate-800">Recommended Job Roles</h3>
              <Link to="/recommendations" className="text-xs font-semibold text-blue-600 hover:underline flex items-center space-x-1">
                <span>View All</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recommendations.slice(0, 4).map((rec, idx) => (
                <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-bold text-slate-800 text-sm">{rec.role}</h4>
                    <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-200">
                      {rec.match_percentage}% Match
                    </span>
                  </div>
                  <p className="text-slate-600 text-xs line-clamp-2">{rec.reason}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
