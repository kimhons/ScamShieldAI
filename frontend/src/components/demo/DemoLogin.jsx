import { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Shield, User, UserCog } from 'lucide-react';

export function DemoLogin() {
  const { setUser } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleDemoLogin = async (userType) => {
    setLoading(true);
    
    // Simulate login delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const demoUser = {
      id: userType === 'admin' ? 'admin-demo-123' : 'client-demo-456',
      email: userType === 'admin' ? 'admin@scamshield.ai' : 'client@scamshield.ai',
      full_name: userType === 'admin' ? 'Admin Demo User' : 'Client Demo User',
      role: userType,
      created_at: new Date().toISOString(),
      subscription_tier: userType === 'admin' ? 'enterprise' : 'premium'
    };
    
    setUser(demoUser);
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-blue-100 rounded-full">
              <Shield className="h-8 w-8 text-blue-600" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">ScamShield AI</h1>
          <p className="text-gray-600 mt-2">Demo Mode - Choose Your Role</p>
        </div>

        <div className="space-y-4">
          <Card className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader className="text-center">
              <div className="flex justify-center mb-2">
                <User className="h-8 w-8 text-green-600" />
              </div>
              <CardTitle className="text-lg">Client Dashboard</CardTitle>
              <CardDescription>
                Access the client interface for creating and managing investigations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={() => handleDemoLogin('client')}
                disabled={loading}
                className="w-full bg-green-600 hover:bg-green-700"
              >
                {loading ? 'Logging in...' : 'Login as Client'}
              </Button>
            </CardContent>
          </Card>

          <Card className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader className="text-center">
              <div className="flex justify-center mb-2">
                <UserCog className="h-8 w-8 text-purple-600" />
              </div>
              <CardTitle className="text-lg">Admin Dashboard</CardTitle>
              <CardDescription>
                Access the admin interface for platform management and analytics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={() => handleDemoLogin('admin')}
                disabled={loading}
                className="w-full bg-purple-600 hover:bg-purple-700"
              >
                {loading ? 'Logging in...' : 'Login as Admin'}
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="text-center text-sm text-gray-500">
          <p>Demo mode - No real authentication required</p>
          <p>All data is simulated for testing purposes</p>
        </div>
      </div>
    </div>
  );
}

