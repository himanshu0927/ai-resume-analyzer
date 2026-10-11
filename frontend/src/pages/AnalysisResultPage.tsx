import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import type { ResumeAnalysis } from '../types';
import { ScoreRing } from '../components/common/ScoreRing';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { 
  Download, 
  User, 
  GraduationCap, 
  Code, 
  FolderGit2, 
  AlertTriangle,
  ArrowLeft
} from 'lucide-react';

export const AnalysisResultPage: React.FC = () => {
  const { resumeId } = useParams<{ resumeId: string }>();
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const res = await api.get<ResumeAnalysis>(`/resumes/${resumeId}/analysis`);
        setAnalysis(res.data);
      } catch (err) {
        console.error("Error fetching analysis:", err);
      } finally {
        setLoading(false);
      }
    };
    if (resumeId) fetchAnalysis();
  }, [resumeId]);

  const handleDownloadPDF = async () => {
    if (!resumeId) return;
    setDownloading(true);
    try {
      const response = await api.post(`/reports/${resumeId}/pdf`, {}, { responseType: 'blob' });
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Resume_Analysis_Report_${resumeId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("PDF download failed", err);
    } finally {
      setDownloading(false);
    }
  };

  if (loading) return <LoadingSkeleton />;
  if (!analysis) {
    return (
      <div className="text-center py-12 space-y-4">
        <h2 className="text-xl font-bold text-slate-800">Analysis Not Found</h2>
        <Link to="/analyzer" className="text-blue-600 font-semibold hover:underline">Back to Resume Analyzer</Link>
      </div>
    );
  }

  const pInfo = analysis.personal_info || { name: 'Candidate', email: 'N/A', phone: 'N/A', location: 'N/A' };
  const rawSkills = analysis.raw_extracted_data?.categorized_skills || {};

  return (
    <div className="space-y-8">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <Link to="/analyzer" className="inline-flex items-center space-x-1 text-xs font-semibold text-slate-500 hover:text-slate-800 mb-1">
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Analyzer</span>
          </Link>
          <h1 className="text-2xl font-bold text-slate-800">Resume Analysis Results</h1>
          <p className="text-xs text-slate-400">Generated for Candidate Profile #{analysis.resume_id}</p>
        </div>

        <button
          onClick={handleDownloadPDF}
          disabled={downloading}
          className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl text-sm transition-all shadow-md shadow-blue-600/20 flex items-center space-x-2 disabled:opacity-50"
        >
          <Download className="w-4 h-4" />
          <span>{downloading ? 'Generating PDF...' : 'Download PDF Report'}</span>
        </button>
      </div>

      {/* Score Overview & Factor Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-xs flex flex-col items-center justify-center space-y-4 lg:col-span-1">
          <ScoreRing score={analysis.overall_score} size={180} label="Resume Analysis Score" />
          
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center text-[11px] text-slate-500 leading-relaxed mt-2">
            <strong>Note:</strong> This is an analytical Resume Score based on structure, skills depth, and content completeness. It does NOT guarantee employment or predict hiring decisions.
          </div>
        </div>

        {/* Contributing Factors */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs lg:col-span-2 space-y-4">
          <h3 className="text-base font-bold text-slate-800">Score Factor Breakdown</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-slate-600 font-semibold">
                  <th className="py-2.5 px-3">Factor</th>
                  <th className="py-2.5 px-3">Weight</th>
                  <th className="py-2.5 px-3">Score</th>
                  <th className="py-2.5 px-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {analysis.score_factors?.map((f, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/60">
                    <td className="py-2.5 px-3 font-medium text-slate-800">{f.factor}</td>
                    <td className="py-2.5 px-3 text-slate-500">{f.weight}</td>
                    <td className="py-2.5 px-3 font-bold text-slate-700">{f.score} / 100</td>
                    <td className="py-2.5 px-3">
                      <span className={`px-2 py-0.5 rounded-md font-semibold text-[11px] ${
                        f.score >= 70 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}>
                        {f.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Candidate Profile Details */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
        <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
          <User className="w-5 h-5 text-blue-600" />
          <span>Extracted Personal Information</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-xs text-slate-400 block font-semibold">Candidate Name</span>
            <span className="font-bold text-slate-800">{pInfo.name}</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-xs text-slate-400 block font-semibold">Email</span>
            <span className="font-bold text-slate-800 truncate block">{pInfo.email}</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-xs text-slate-400 block font-semibold">Phone</span>
            <span className="font-bold text-slate-800">{pInfo.phone}</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-xs text-slate-400 block font-semibold">Location</span>
            <span className="font-bold text-slate-800">{pInfo.location}</span>
          </div>
        </div>
      </div>

      {/* Categorized Skills Section */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-6">
        <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
          <Code className="w-5 h-5 text-indigo-600" />
          <span>Categorized Technical & Soft Skills</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(rawSkills).map(([cat, skills]) => (
            skills.length > 0 && (
              <div key={cat} className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">{cat}</h4>
                <div className="flex flex-wrap gap-1.5">
                  {skills.map((s, sIdx) => (
                    <span key={sIdx} className="px-2.5 py-1 bg-white text-slate-800 font-semibold text-xs rounded-md border border-slate-200 shadow-2xs">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )
          ))}
        </div>
      </div>

      {/* Experience & Education */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Education */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
            <GraduationCap className="w-5 h-5 text-purple-600" />
            <span>Academic Background</span>
          </h3>
          <div className="space-y-3">
            {analysis.education?.map((edu, idx) => (
              <div key={idx} className="p-4 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
                <h4 className="font-bold text-slate-800 text-sm">{edu.degree}</h4>
                <p className="text-xs text-slate-600">{edu.institution} • {edu.graduation_year}</p>
                <p className="text-xs text-slate-400">Coursework: {edu.relevant_coursework}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Projects */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
            <FolderGit2 className="w-5 h-5 text-emerald-600" />
            <span>Key Projects</span>
          </h3>
          <div className="space-y-3">
            {analysis.projects?.map((proj, idx) => (
              <div key={idx} className="p-4 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
                <h4 className="font-bold text-slate-800 text-sm">{proj.project_name}</h4>
                <p className="text-xs font-semibold text-blue-600">Tech Stack: {proj.technologies}</p>
                <p className="text-xs text-slate-600 line-clamp-2">{proj.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Prioritized Improvement Suggestions */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
        <h3 className="text-base font-bold text-slate-800 flex items-center space-x-2">
          <AlertTriangle className="w-5 h-5 text-amber-500" />
          <span>Prioritized Improvement Suggestions</span>
        </h3>

        <div className="space-y-3">
          {analysis.suggestions?.map((sug, idx) => (
            <div 
              key={idx} 
              className={`p-4 rounded-xl border flex items-start space-x-3 text-sm ${
                sug.priority === 'High' ? 'bg-red-50/50 border-red-200 text-red-900' :
                sug.priority === 'Medium' ? 'bg-amber-50/50 border-amber-200 text-amber-900' :
                'bg-blue-50/50 border-blue-200 text-blue-900'
              }`}
            >
              <span className={`px-2 py-0.5 rounded-md font-bold text-[10px] uppercase tracking-wider flex-shrink-0 mt-0.5 ${
                sug.priority === 'High' ? 'bg-red-600 text-white' :
                sug.priority === 'Medium' ? 'bg-amber-600 text-white' :
                'bg-blue-600 text-white'
              }`}>
                {sug.priority} Priority
              </span>
              <p className="font-medium text-xs sm:text-sm leading-relaxed">{sug.text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
