import React from 'react';

interface ScoreRingProps {
  score: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
}

export const ScoreRing: React.FC<ScoreRingProps> = ({
  score,
  size = 140,
  strokeWidth = 12,
  label = "Resume Analysis Score"
}) => {
  const center = size / 2;
  const radius = center - strokeWidth;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let color = "#10B981"; // Emerald green
  if (score < 60) color = "#EF4444"; // Red
  else if (score < 75) color = "#F59E0B"; // Amber

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative inline-flex items-center justify-center">
        <svg width={size} height={size} className="transform -rotate-90">
          <circle
            cx={center}
            cy={center}
            r={radius}
            stroke="#E2E8F0"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          <circle
            cx={center}
            cy={center}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-bold text-slate-800 tracking-tight">{score}</span>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Out of 100</span>
        </div>
      </div>
      {label && <p className="mt-3 text-sm font-semibold text-slate-600">{label}</p>}
    </div>
  );
};
