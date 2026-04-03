import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import ChatbotWidget from './chatbot/ChatbotWidget';

// Public Pages
import Home from './pages/public/Home';
import About from './pages/public/About';
import Login from './pages/public/Login';

// Student Pages (Placeholders implementation will follow)
import StudentDashboard from './pages/student/Dashboard';
// Admin Pages (Placeholders)
import AdminDashboard from './pages/admin/Dashboard';

const ProtectedRoute = ({ children, roleRequired }) => {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading portal...</div>;
  if (!user) return <Navigate to="/login" />;
  if (roleRequired && user.role !== roleRequired) return <Navigate to="/" />;

  return children;
};

// Routes where the chatbot must NOT appear
const PUBLIC_ROUTES = ['/', '/about', '/login'];

function AppContent() {
  const { user } = useAuth();
  const { pathname } = useLocation();

  // Show chatbot ONLY on the Home page
  const showChatbot = pathname === '/';

  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Routes>
        <Route path="/student/*" element={null} />
        <Route path="/admin/*" element={null} />
        <Route path="*" element={<Navbar />} />
      </Routes>

      <main style={{ flex: 1 }}>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />

          {/* Student Routes */}
          <Route path="/student/*" element={
            <ProtectedRoute roleRequired="student">
              <StudentDashboard />
            </ProtectedRoute>
          } />

          {/* Admin Routes */}
          <Route path="/admin/*" element={
            <ProtectedRoute roleRequired="admin">
              <AdminDashboard />
            </ProtectedRoute>
          } />
        </Routes>
      </main>

      {/* Show chatbot only on protected/dashboard pages */}
      {showChatbot && <ChatbotWidget />}
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
