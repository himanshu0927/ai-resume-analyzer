import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Mail, Calendar } from 'lucide-react';

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-800">Candidate Profile</h1>
        <p className="text-slate-500 text-sm mt-1">Manage your account information and authentication credentials.</p>
      </div>

      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-xs space-y-6">
        <div className="flex items-center space-x-4 border-b border-slate-100 pb-6">
          <div className="w-16 h-16 rounded-full bg-blue-100 text-blue-700 font-bold text-2xl flex items-center justify-center border-2 border-blue-200 shadow-inner">
            {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">{user?.name}</h2>
            <p className="text-xs text-slate-400 font-medium">{user?.email}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
            <span className="text-xs text-slate-400 font-semibold block flex items-center space-x-1">
              <Mail className="w-3.5 h-3.5" />
              <span>Email Address</span>
            </span>
            <p className="font-bold text-slate-800 text-sm">{user?.email}</p>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
            <span className="text-xs text-slate-400 font-semibold block flex items-center space-x-1">
              <Calendar className="w-3.5 h-3.5" />
              <span>Account Created</span>
            </span>
            <p className="font-bold text-slate-800 text-sm">
              {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Active Candidate'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
