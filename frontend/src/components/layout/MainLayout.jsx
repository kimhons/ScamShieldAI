import { useAuth } from '../../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import { LoadingSpinner } from '../ui/LoadingSpinner';

export function MainLayout({ children, requireAuth = true, requiredRole = null }) {
  const { user, loading, isAdmin } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (requireAuth && !user) {
    return <Navigate to="/auth/login" replace />;
  }

  if (requiredRole === 'admin' && !isAdmin) {
    return <Navigate to="/unauthorized" replace />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {children}
    </div>
  );
}

