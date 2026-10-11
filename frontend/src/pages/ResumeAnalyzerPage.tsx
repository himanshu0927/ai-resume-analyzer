import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Upload, AlertCircle, CheckCircle, Sparkles } from 'lucide-react';

export const ResumeAnalyzerPage: React.FC = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile: File) => {
    setError('');
    const ext = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();
    if (!['.pdf', '.docx', '.doc'].includes(ext)) {
      setError('Invalid file format. Please upload a PDF (.pdf) or Word document (.docx).');
      setFile(null);
      return;
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10MB limit.');
      setFile(null);
      return;
    }
    setFile(selectedFile);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post('/resumes/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const resumeId = res.data.id;
      navigate(`/analysis/${resumeId}`);
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to parse and analyze document. Please check the file.';
      setError(msg);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-slate-800">Resume Analyzer</h1>
        <p className="text-slate-500 text-sm max-w-xl mx-auto">
          Upload your resume in PDF or Word format to extract technical skills, calculate structural scores, and receive actionable suggestions.
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start space-x-3 text-red-700 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-xs">
        <form onSubmit={handleUpload} className="space-y-6">
          {/* Dropzone */}
          <div
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            className={`
              border-2 border-dashed rounded-2xl p-10 text-center transition-all cursor-pointer flex flex-col items-center justify-center space-y-4
              ${dragActive ? 'border-blue-500 bg-blue-50/50 scale-[1.01]' : 'border-slate-300 hover:border-blue-400 bg-slate-50/50'}
            `}
            onClick={() => document.getElementById('file-upload-input')?.click()}
          >
            <input
              id="file-upload-input"
              type="file"
              accept=".pdf,.docx,.doc"
              onChange={handleFileChange}
              className="hidden"
            />
            
            <div className="w-16 h-16 rounded-2xl bg-blue-100 text-blue-600 flex items-center justify-center shadow-inner">
              <Upload className="w-8 h-8" />
            </div>

            {file ? (
              <div className="space-y-1">
                <div className="flex items-center justify-center space-x-2 text-emerald-600 font-bold text-base">
                  <CheckCircle className="w-5 h-5" />
                  <span>{file.name}</span>
                </div>
                <p className="text-xs text-slate-400">{(file.size / (1024 * 1024)).toFixed(2)} MB • Ready to analyze</p>
              </div>
            ) : (
              <div className="space-y-1">
                <p className="text-slate-700 font-semibold text-base">
                  Click to upload or drag & drop resume file
                </p>
                <p className="text-xs text-slate-400">Supports PDF or DOCX up to 10MB</p>
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={!file || uploading}
            className="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl text-base transition-all shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {uploading ? (
              <div className="flex items-center space-x-3">
                <span className="inline-block animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></span>
                <span>Extracting Text & Analyzing Skills...</span>
              </div>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Start Resume Analysis</span>
              </>
            )}
          </button>
        </form>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
        <div className="p-5 bg-white border border-slate-200 rounded-xl space-y-2">
          <h4 className="font-bold text-slate-800 text-sm">Real Text Extraction</h4>
          <p className="text-xs text-slate-500">Extracts actual text from PDF and DOCX files using local parsing engines.</p>
        </div>
        <div className="p-5 bg-white border border-slate-200 rounded-xl space-y-2">
          <h4 className="font-bold text-slate-800 text-sm">Skills Categorization</h4>
          <p className="text-xs text-slate-500">Maps candidate skills to 9 distinct technical & soft skill taxonomy domains.</p>
        </div>
        <div className="p-5 bg-white border border-slate-200 rounded-xl space-y-2">
          <h4 className="font-bold text-slate-800 text-sm">Score Factors</h4>
          <p className="text-xs text-slate-500">Calculates weighted factor scores from 0–100 with actionable feedback.</p>
        </div>
      </div>
    </div>
  );
};
