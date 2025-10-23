import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import NumerologyPage from './pages/NumerologyPage';
import ZodiacPage from './pages/ZodiacPage';
import LoveMatchPage from './pages/LoveMatchPage';
import TarotPage from './pages/TarotPage';
import DailyFortunePage from './pages/DailyFortunePage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';
import StarBackground from './components/common/StarBackground';
import ProtectedRoute from './components/auth/ProtectedRoute';

function AppContent() {
  const { user } = useAuth();

  useEffect(() => {
    // Apply theme from user settings
    const theme = user?.theme_preference || 'galaxy';
    
    const themeColors: Record<string, { bg: string, accent: string }> = {
      galaxy: { bg: 'linear-gradient(to bottom, #0a0118, #1a0a2e)', accent: '#8a2be2' },
      nebula: { bg: 'linear-gradient(to bottom, #0d0221, #1a0d33)', accent: '#4b0082' },
      sunrise: { bg: 'linear-gradient(to bottom, #1a0f08, #2d1810)', accent: '#ffd700' },
      ocean: { bg: 'linear-gradient(to bottom, #001a33, #002244)', accent: '#1e90ff' },
      forest: { bg: 'linear-gradient(to bottom, #0a1f0a, #133013)', accent: '#228b22' },
      sunset: { bg: 'linear-gradient(to bottom, #1a0808, #2d1010)', accent: '#ff6347' }
    };
    
    const themeStyle = themeColors[theme];
    if (themeStyle) {
      document.body.style.background = themeStyle.bg;
      document.body.style.backgroundAttachment = 'fixed';
      document.documentElement.style.setProperty('--theme-accent', themeStyle.accent);
    }
  }, [user]);

  return (
    <Router>
      <StarBackground />
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout>
                    <HomePage />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/numerology"
              element={
                <ProtectedRoute>
                  <Layout>
                    <NumerologyPage />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/zodiac"
              element={
                <ProtectedRoute>
                  <Layout>
                    <ZodiacPage />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/love"
              element={
                <ProtectedRoute>
                  <Layout>
                    <LoveMatchPage />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/tarot"
              element={
                <ProtectedRoute>
                  <Layout>
                    <TarotPage />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/daily"
              element={
                <ProtectedRoute>
                  <Layout>
                    <DailyFortunePage />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/history"
              element={
                <ProtectedRoute>
                  <Layout>
                    <HistoryPage />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/settings"
              element={
                <ProtectedRoute>
                  <Layout>
                    <SettingsPage />
                  </Layout>
                </ProtectedRoute>
              }
            />
          </Routes>
        </AnimatePresence>
      </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;