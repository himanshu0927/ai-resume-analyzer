import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { DashboardLayout } from './components/layout/DashboardLayout';

import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';
import { ResumeAnalyzerPage } from './pages/ResumeAnalyzerPage';
import { AnalysisResultPage } from './pages/AnalysisResultPage';
import { JobMatcherPage } from './pages/JobMatcherPage';
import { SkillGapPage } from './pages/SkillGapPage';
import { JobRecommendationsPage } from './pages/JobRecommendationsPage';
import { AnalysisHistoryPage } from './pages/AnalysisHistoryPage';
import { ProfilePage } from './pages/ProfilePage';
import { SettingsPage } from './pages/SettingsPage';

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Dashboard Routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/analyzer" element={<ResumeAnalyzerPage />} />
              <Route path="/analysis/:resumeId" element={<AnalysisResultPage />} />
              <Route path="/job-matcher" element={<JobMatcherPage />} />
              <Route path="/skill-gap" element={<SkillGapPage />} />
              <Route path="/recommendations" element={<JobRecommendationsPage />} />
              <Route path="/history" element={<AnalysisHistoryPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
          </Route>

          {/* Fallback Catch-all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
