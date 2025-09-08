import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { MainLayout } from './components/layout/MainLayout';
import { LoginForm } from './components/auth/LoginForm';
import { RegisterForm } from './components/auth/RegisterForm';
import { ClientDashboard } from './components/client/ClientDashboard';
import { AdminDashboard } from './components/admin/AdminDashboard';
import { ErrorBoundary } from './components/ui/ErrorBoundary';
import { DemoLogin } from './components/demo/DemoLogin';
import { useAuth } from './contexts/AuthContext';
import './App.css';

function AppRoutes() {
  const { user, loading, isAdmin } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-2 border-gray-300 border-t-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 font-medium">Loading ScamShield AI...</p>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      {/* Demo Route */}
      <Route path="/demo" element={<DemoLogin />} />
      
      {/* Public routes */}
      <Route path="/auth/login" element={
        user ? <Navigate to="/dashboard" replace /> : <LoginForm />
      } />
      <Route path="/auth/register" element={
        user ? <Navigate to="/dashboard" replace /> : <RegisterForm />
      } />
      
      {/* Protected routes */}
      <Route path="/dashboard" element={
        <MainLayout requireAuth={true}>
          {isAdmin ? <AdminDashboard /> : <ClientDashboard />}
        </MainLayout>
      } />
      
      <Route path="/admin/*" element={
        <MainLayout requireAuth={true} requiredRole="admin">
          <AdminDashboard />
        </MainLayout>
      } />
      
      <Route path="/client/*" element={
        <MainLayout requireAuth={true}>
          <ClientDashboard />
        </MainLayout>
      } />
      
      {/* Default redirects */}
      <Route path="/" element={
        user ? <Navigate to="/dashboard" replace /> : <Navigate to="/demo" replace />
      } />
      
      {/* Unauthorized page */}
      <Route path="/unauthorized" element={
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Unauthorized</h1>
            <p className="text-gray-600 mb-4">You don't have permission to access this page.</p>
            <button 
              onClick={() => window.history.back()}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Go Back
            </button>
          </div>
        </div>
      } />
      
      {/* 404 page */}
      <Route path="*" element={
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Page Not Found</h1>
            <p className="text-gray-600 mb-4">The page you're looking for doesn't exist.</p>
            <button 
              onClick={() => window.history.back()}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Go Back
            </button>
          </div>
        </div>
      } />
    </Routes>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </Router>
    </ErrorBoundary>
  );
}

export default App;

