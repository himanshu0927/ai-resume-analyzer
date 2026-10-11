import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import type { Resume, ResumeAnalysis } from '../types';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { 
  Eye, 
  Trash2, 
  Download, 
  FileText, 
  PlusCircle 
} from 'lucide-react';

interface CombinedHistoryItem {
  resume: Resume;
  analysis?: ResumeAnalysis;
}

export const AnalysisHistoryPage: React.FC = () => {
  const [historyItems, setHistoryItems] = useState<CombinedHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const fetchHistory = async () => {
    try {
      const resRes = await api.get<Resume[]>('/resumes');
      const items: CombinedHistoryItem[] = [];

      for (const r of resRes.data) {
        try {
          const aRes = await api.get<ResumeAnalysis>(`/resumes/${r.id}/analysis`);
          items.push({ resume: r, analysis: aRes.data });
        } catch (e) {
          items.push({ resume: r });
        }
      }
      setHistoryItems(items);
    } catch (err) {
      console.error("Error loading history", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (resumeId: number) => {
    if (!window.confirm("Are you sure you want to delete this resume analysis record?")) return;
    setDeletingId(resumeId);
    try {
      await api.delete(`/resumes/${resumeId}`);
      setHistoryItems(prev => prev.filter(i => i.resume.id !== resumeId));
    } catch (err) {
      console.error("Failed to delete resume", err);
    } finally {
      setDeletingId(null);
    }
  };

  const handleDownloadPDF = async (resumeId: number) => {
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
    }
  };

  if (loading) return <LoadingSkeleton />;

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-800">My Resume Analyses</h1>
          <p className="text-slate-500 text-sm mt-1">
            Historical records of parsed documents, calculated scores, and PDF reports.
          </p>
        </div>

        <Link
          to="/analyzer"
          className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl text-sm transition-all shadow-md shadow-blue-600/20 flex items-center space-x-2"
        >
          <PlusCircle className="w-4 h-4" />
          <span>Analyze New Resume</span>
        </Link>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        {historyItems.length === 0 ? (
          <div className="text-center py-16 space-y-4">
            <div className="w-12 h-12 rounded-xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
              <FileText className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-700">No Resume Analyses Found</h3>
            <p className="text-xs text-slate-400">Upload your first resume to generate a score report.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-slate-600 font-semibold text-xs uppercase tracking-wider">
                  <th className="py-3.5 px-4">Resume Name</th>
                  <th className="py-3.5 px-4">Upload Date</th>
                  <th className="py-3.5 px-4">Analysis Score</th>
                  <th className="py-3.5 px-4">Detected Skills</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {historyItems.map(({ resume, analysis }) => (
                  <tr key={resume.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-4 px-4 font-bold text-slate-800 flex items-center space-x-2">
                      <FileText className="w-4 h-4 text-blue-600 flex-shrink-0" />
                      <span className="truncate max-w-xs">{resume.filename}</span>
                    </td>
                    <td className="py-4 px-4 text-xs text-slate-500">
                      {new Date(resume.uploaded_at).toLocaleDateString()}
                    </td>
                    <td className="py-4 px-4">
                      {analysis ? (
                        <span className={`px-2.5 py-1 rounded-lg font-bold text-xs ${
                          analysis.overall_score >= 80 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                          analysis.overall_score >= 60 ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                          'bg-red-50 text-red-700 border border-red-200'
                        }`}>
                          {analysis.overall_score} / 100
                        </span>
                      ) : (
                        <span className="text-xs text-slate-400">Processing</span>
                      )}
                    </td>
                    <td className="py-4 px-4 font-semibold text-slate-700">
                      {analysis?.raw_extracted_data?.total_count || 0} Skills
                    </td>
                    <td className="py-4 px-4 text-right">
                      <div className="flex items-center justify-end space-x-2">
                        <Link
                          to={`/analysis/${resume.id}`}
                          className="p-2 text-slate-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="View Analysis"
                        >
                          <Eye className="w-4 h-4" />
                        </Link>
                        <button
                          onClick={() => handleDownloadPDF(resume.id)}
                          className="p-2 text-slate-600 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
                          title="Download PDF"
                        >
                          <Download className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(resume.id)}
                          disabled={deletingId === resume.id}
                          className="p-2 text-slate-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                          title="Delete Record"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
