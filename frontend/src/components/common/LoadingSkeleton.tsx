import React from 'react';

export const LoadingSkeleton: React.FC = () => {
  return (
    <div className="animate-pulse space-y-6 p-6 bg-white rounded-xl shadow-sm border border-slate-200">
      <div className="h-8 bg-slate-200 rounded w-1/3"></div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="h-28 bg-slate-200 rounded-lg"></div>
        <div className="h-28 bg-slate-200 rounded-lg"></div>
        <div className="h-28 bg-slate-200 rounded-lg"></div>
      </div>
      <div className="h-64 bg-slate-200 rounded-lg"></div>
    </div>
  );
};
