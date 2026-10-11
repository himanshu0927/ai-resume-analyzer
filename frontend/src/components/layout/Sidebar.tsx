import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  Briefcase, 
  Target, 
  Lightbulb, 
  History, 
  User, 
  Settings as SettingsIcon,
  LogOut
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, setIsOpen }) => {
  const { logout } = useAuth();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Resume Analyzer', path: '/analyzer', icon: FileText },
    { name: 'Job Matcher', path: '/job-matcher', icon: Briefcase },
    { name: 'Skill Gap', path: '/skill-gap', icon: Target },
    { name: 'Job Recommendations', path: '/recommendations', icon: Lightbulb },
    { name: 'My Analyses', path: '/history', icon: History },
    { name: 'Profile', path: '/profile', icon: User },
    { name: 'Settings', path: '/settings', icon: SettingsIcon },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-slate-900/50 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      <aside className={`
        fixed top-0 left-0 z-50 h-full w-64 bg-slate-900 text-slate-300 transform transition-transform duration-200 ease-in-out
        lg:translate-x-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        flex flex-col justify-between border-r border-slate-800
      `}>
        <div>
          {/* Logo */}
          <div className="h-16 flex items-center px-6 border-b border-slate-800 space-x-3">
            <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-lg shadow-md shadow-blue-500/20">
              AI
            </div>
            <div>
              <h1 className="font-bold text-white text-base leading-tight">Resume AI</h1>
              <p className="text-xs text-slate-400">Career Match Engine</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1.5 overflow-y-auto">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) => `
                  flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors
                  ${isActive 
                    ? 'bg-blue-600 text-white font-semibold shadow-sm' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'}
                `}
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Footer Logout */}
        <div className="p-4 border-t border-slate-800">
          <button
            onClick={logout}
            className="w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-red-400 hover:bg-slate-800/60 transition-colors"
          >
            <LogOut className="w-5 h-5 flex-shrink-0" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>
    </>
  );
};
