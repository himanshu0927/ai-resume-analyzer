import React, { useEffect, useState } from 'react';
import api from '../services/api';
import type { Resume, JobMatch } from '../types';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { 
  CheckCircle, 
  XCircle, 
  Sparkles, 
  AlertCircle,
  Lightbulb
} from 'lucide-react';

export const JobMatcherPage: React.FC = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState<number | undefined>(undefined);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  
  const [loading, setLoading] = useState(true);
  const [matching, setMatching] = useState(false);
  const [matchResult, setMatchResult] = useState<JobMatch | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await api.get<Resume[]>('/resumes');
        setResumes(res.data);
        if (res.data.length > 0) {
          setSelectedResumeId(res.data[0].id);
        }
      } catch (err) {
        console.error("Error loading resumes", err);
      } finally {
        setLoading(false);
      }
    };
    fetchResumes();
  }, []);

  const handleMatch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobTitle.trim() || !jobDescription.trim()) {
      setError('Please provide both Job Title and Job Description.');
      return;
    }

    setMatching(true);
    setError('');

    try {
      const res = await api.post<JobMatch>('/job-match', {
        resume_id: selectedResumeId,
        job_title: jobTitle,
        job_description: jobDescription
      });
      setMatchResult(res.data);
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Job matching failed. Please check inputs.';
      setError(msg);
    } finally {
      setMatching(false);
    }
  };

  if (loading) return <LoadingSkeleton />;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-slate-800">Job Matcher</h1>
        <p className="text-slate-500 text-sm max-w-xl mx-auto">
          Compare your resume against any job description to evaluate keyword coverage, technical skill alignment, and targeted improvement suggestions.
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start space-x-3 text-red-700 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {/* Input Form */}
      <div className="bg-white p-6 md:p-8 rounded-2xl border border-slate-200 shadow-xs">
        <form onSubmit={handleMatch} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Target Job Title</label>
              <input
                type="text"
                required
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Full Stack Engineer"
                className="w-full px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-slate-800 placeholder-slate-400 focus:outline-hidden focus:border-blue-500 transition-colors text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Select Analyzed Resume</label>
              <select
                value={selectedResumeId || ''}
                onChange={(e) => setSelectedResumeId(Number(e.target.value))}
                className="w-full px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-slate-800 focus:outline-hidden focus:border-blue-500 transition-colors text-sm"
              >
                {resumes.map(r => (
                  <option key={r.id} value={r.id}>
                    {r.filename} (Uploaded: {new Date(r.uploaded_at).toLocaleDateString()})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Job Description</label>
            <textarea
              required
              rows={6}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full target job description text here..."
              className="w-full px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-slate-800 placeholder-slate-400 focus:outline-hidden focus:border-blue-500 transition-colors text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={matching}
            className="w-full py-3.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl text-sm transition-all shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {matching ? (
              <div className="flex items-center space-x-2">
                <span className="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></span>
                <span>Calculating Match Matrix...</span>
              </div>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Compare & Match Job</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Match Results Display */}
      {matchResult && (
        <div className="space-y-8 animate-fadeIn">
          {/* Header Score Card */}
          <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-8 rounded-2xl border border-slate-800 text-white flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
            <div className="space-y-2 text-center md:text-left">
              <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold rounded-full uppercase tracking-wider">
                Job Match Analysis
              </span>
              <h2 className="text-2xl font-bold">{matchResult.job_title}</h2>
              <p className="text-xs text-slate-400 max-w-lg">
                Calculated by cross-referencing candidate technical skills and keyword context against target role requirements.
              </p>
            </div>

            <div className="flex flex-col items-center justify-center bg-slate-800/80 p-6 rounded-2xl border border-slate-700 min-w-[160px]">
              <span className="text-4xl font-extrabold text-blue-400">{matchResult.match_score}%</span>
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mt-1">Match Rating</span>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-center text-xs text-amber-800 font-medium">
            <strong>Disclaimer:</strong> This match rating is an analytical keyword comparison tool to help tailor your resume and does NOT guarantee employment or predict hiring decisions.
          </div>

          {/* Skills Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Matching Skills */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-emerald-500" />
                <span>Matching Skills ({matchResult.matching_skills.length})</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {matchResult.matching_skills.map((s, idx) => (
                  <span key={idx} className="px-3 py-1.5 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-lg border border-emerald-200 flex items-center space-x-1">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>{s}</span>
                  </span>
                ))}
              </div>
            </div>

            {/* Missing Skills */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
                <XCircle className="w-5 h-5 text-red-500" />
                <span>Missing Skills ({matchResult.missing_skills.length})</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {matchResult.missing_skills.map((s, idx) => (
                  <span key={idx} className="px-3 py-1.5 bg-red-50 text-red-700 text-xs font-semibold rounded-lg border border-red-200 flex items-center space-x-1">
                    <XCircle className="w-3.5 h-3.5" />
                    <span>{s}</span>
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Suggestions */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
            <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
              <Lightbulb className="w-5 h-5 text-blue-600" />
              <span>Tailored Suggestions for Improvement</span>
            </h3>
            <div className="space-y-3">
              {matchResult.suggestions?.map((sug, idx) => (
                <div key={idx} className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-sm space-y-1">
                  <span className="text-xs font-bold text-blue-600 uppercase tracking-wider block">{sug.type}</span>
                  <p className="text-slate-700 text-xs sm:text-sm">{sug.text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
