import React from 'react';
import { Menu, User } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { Link } from 'react-router-dom';

interface NavbarProps {
  onMenuClick: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onMenuClick }) => {
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-30 h-16 bg-white border-b border-slate-200 px-4 lg:px-8 flex items-center justify-between shadow-xs">
      <div className="flex items-center space-x-4">
        <button
          onClick={onMenuClick}
          className="p-2 rounded-lg text-slate-600 hover:bg-slate-100 lg:hidden"
          aria-label="Toggle menu"
        >
          <Menu className="w-6 h-6" />
        </button>
        <div className="hidden sm:block">
          <h2 className="text-sm font-semibold text-slate-700">AI Resume Analyzer & Job Matcher</h2>
        
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <div className="hidden md:flex items-center space-x-2 bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-semibold border border-emerald-200">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
          <span>Engine Active</span>
        </div>

        <div className="flex items-center space-x-3 pl-4 border-l border-slate-200">
          <Link to="/profile" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div className="w-9 h-9 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center border border-blue-200">
              {user?.name ? user.name.charAt(0).toUpperCase() : <User className="w-4 h-4" />}
            </div>
            <div className="hidden md:block text-left">
              <div className="text-xs font-bold text-slate-800">{user?.name || 'User'}</div>
              <div className="text-[11px] text-slate-400 truncate max-w-[140px]">{user?.email || 'Candidate'}</div>
            </div>
          </Link>
        </div>
      </div>
    </header>
  );
};
