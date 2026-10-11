import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Briefcase, 
  Target, 
  ArrowRight, 
  Sparkles
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      {/* Header Nav */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-lg shadow-md shadow-blue-500/20">
              AI
            </div>
            <span className="font-bold text-lg text-white">AI Resume Analyzer</span>
          </div>

          <div className="flex items-center space-x-4">
            <Link to="/login" className="px-4 py-2 text-sm font-semibold text-slate-300 hover:text-white transition-colors">
              Sign In
            </Link>
            <Link 
              to="/register" 
              className="px-4 py-2 text-sm font-semibold bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-all shadow-md shadow-blue-600/30"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="max-w-5xl mx-auto px-6 text-center relative z-10">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-6">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI-Powered Career Intelligence</span>
          </div>
          
          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight">
            Turn Your Resume Into Your <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
              Career Roadmap
            </span>
          </h1>
          
          <p className="mt-6 text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
            Analyze your resume, identify skill gaps, and understand how your profile matches your target roles using local NLP and intelligent keyword algorithms.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link 
              to="/register" 
              className="w-full sm:w-auto px-8 py-3.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl text-base transition-all shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2"
            >
              <span>Analyze Resume</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link 
              to="/login" 
              className="w-full sm:w-auto px-8 py-3.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl text-base border border-slate-700 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Highlights */}
      <section className="py-20 bg-slate-950 border-t border-slate-800/80">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-white">Complete Career Intelligence Suite</h2>
            <p className="mt-3 text-slate-400">Built as a production-grade full-stack solution with real-time text parsing, transparent scoring, and actionable recommendations.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-slate-700 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-6">
                <FileText className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Resume Analysis & Scoring</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Extract technical skills, work experience, education, and projects with transparent 0–100 Resume Analysis Scores.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-slate-700 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-6">
                <Briefcase className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Job Description Matcher</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Compare candidate resumes directly against custom target job descriptions to compute similarity, matching skills, and missing requirements.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-slate-700 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-6">
                <Target className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Skill Gap & Role Roadmap</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Compare current candidate skills vs industry standard target roles with suggested learning topics and practical project ideas.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-slate-900 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-white">How It Works</h2>
            <p className="mt-3 text-slate-400">Simple 4-step workflow to unlock insights from your document.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              { step: '01', title: 'Upload Resume', desc: 'Support PDF and DOCX formats with instant text extraction.' },
              { step: '02', title: 'NLP Extraction', desc: 'Categorizes technical skills, projects, education & work history.' },
              { step: '03', title: 'Score & Match', desc: 'Computes transparent Resume Score and matches target job descriptions.' },
              { step: '04', title: 'PDF Report', desc: 'Generates comprehensive analysis report ready for download.' }
            ].map((s, idx) => (
              <div key={idx} className="bg-slate-950/60 border border-slate-800 p-6 rounded-xl relative">
                <span className="text-4xl font-extrabold text-blue-500/20 mb-2 block">{s.step}</span>
                <h4 className="text-lg font-bold text-white mb-2">{s.title}</h4>
                <p className="text-slate-400 text-xs leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20 bg-slate-950 border-t border-slate-800">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-white text-center mb-12">Frequently Asked Questions</h2>
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
              <h4 className="text-base font-bold text-white">Does this tool guarantee a job offer?</h4>
              <p className="mt-2 text-slate-400 text-sm">No. The system calculates an analytical Resume Score and keyword match ratio for informational self-improvement and does not predict hiring decisions.</p>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
              <h4 className="text-base font-bold text-white">Which document formats are supported?</h4>
              <p className="mt-2 text-slate-400 text-sm">PDF (.pdf) and Microsoft Word (.docx) files up to 10MB.</p>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
              <h4 className="text-base font-bold text-white">How is skill extraction performed?</h4>
              <p className="mt-2 text-slate-400 text-sm">Uses local spaCy/regex taxonomy matching with fallback LLM API integration when configured in environment variables.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800 py-8 bg-slate-950 text-slate-500 text-sm text-center">
        <div className="max-w-7xl mx-auto px-6">
          <p>© 2026 AI Resume Analyzer & Job Matcher. B.Tech Final Year Project.</p>
        </div>
      </footer>
    </div>
  );
};
