import { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useDashboard } from '../../hooks/useDashboard';
import { useInvestigations } from '../../hooks/useInvestigations';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { LoadingSpinner, LoadingSkeleton } from '../ui/LoadingSpinner';
import { InvestigationModal } from './InvestigationModal';
import { 
  Shield, 
  Search, 
  FileText, 
  AlertTriangle, 
  Plus,
  TrendingUp,
  Clock,
  CheckCircle,
  Eye,
  Download
} from 'lucide-react';

export function ClientDashboard() {
  const { user, logout } = useAuth();
  const { dashboardData, loading: dashboardLoading } = useDashboard();
  const { investigations, loading: investigationsLoading } = useInvestigations();
  const [showInvestigationModal, setShowInvestigationModal] = useState(false);

  const handleLogout = async () => {
    await logout();
  };

  if (dashboardLoading) {
    return <DashboardSkeleton />;
  }

  const stats = dashboardData?.stats || {};
  const recentInvestigations = investigations.slice(0, 3);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white/95 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <Shield className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                ScamShield AI
              </span>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white font-semibold">
                  {user?.user_metadata?.full_name?.[0] || user?.email?.[0]?.toUpperCase()}
                </div>
                <div>
                  <p className="font-medium text-gray-900">
                    {user?.user_metadata?.full_name || 'User'}
                  </p>
                  <p className="text-xs text-gray-500">Pro Plan</p>
                </div>
              </div>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 border border-gray-200">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Welcome back, {user?.user_metadata?.full_name?.split(' ')[0] || 'User'}!
                </h1>
                <p className="text-gray-600 mt-1">Your digital protection is active and monitoring</p>
              </div>
              <div className="flex items-center gap-2 bg-green-50 text-green-700 px-3 py-2 rounded-full text-sm font-medium">
                <CheckCircle className="h-4 w-4" />
                Protected
              </div>
            </div>
            
            {/* Quick Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-xl border border-blue-100">
                <div className="text-2xl font-bold text-blue-600">{stats.totalInvestigations || 0}</div>
                <div className="text-sm text-gray-600">Total Scans</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-xl border border-green-100">
                <div className="text-2xl font-bold text-green-600">{stats.completedInvestigations || 0}</div>
                <div className="text-sm text-gray-600">Completed</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-xl border border-yellow-100">
                <div className="text-2xl font-bold text-yellow-600">{stats.pendingInvestigations || 0}</div>
                <div className="text-sm text-gray-600">In Progress</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-xl border border-purple-100">
                <div className="text-2xl font-bold text-purple-600">{stats.credits || 0}</div>
                <div className="text-sm text-gray-600">Credits</div>
              </div>
            </div>
          </div>
        </div>

        {/* Action Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card 
            className="cursor-pointer hover:shadow-lg transition-all duration-200 bg-gradient-to-br from-blue-600 to-purple-600 text-white border-0"
            onClick={() => setShowInvestigationModal(true)}
          >
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-white/20 rounded-lg">
                  <Search className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">New Investigation</h3>
                  <p className="text-blue-100 text-sm">Scan emails, phones, domains & more</p>
                </div>
              </div>
              <Button variant="secondary" className="w-full mt-4 bg-white/20 hover:bg-white/30 text-white border-white/30">
                <Plus className="h-4 w-4 mr-2" />
                Start Scan
              </Button>
            </CardContent>
          </Card>

          <Card className="cursor-pointer hover:shadow-lg transition-all duration-200">
            <CardContent className="p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <FileText className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">View Reports</h3>
                  <p className="text-gray-600 text-sm">Access your investigation reports</p>
                </div>
              </div>
              <Button variant="outline" className="w-full">
                <Eye className="h-4 w-4 mr-2" />
                View All Reports
              </Button>
            </CardContent>
          </Card>

          <Card className="cursor-pointer hover:shadow-lg transition-all duration-200">
            <CardContent className="p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="p-3 bg-red-100 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-red-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Security Alerts</h3>
                  <p className="text-gray-600 text-sm">Monitor threats and warnings</p>
                </div>
              </div>
              <Button variant="outline" className="w-full">
                <AlertTriangle className="h-4 w-4 mr-2" />
                View Alerts
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Recent Investigations */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle>Recent Investigations</CardTitle>
                <CardDescription>Your latest scam detection scans</CardDescription>
              </div>
              <Button variant="outline" size="sm">
                View All
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {investigationsLoading ? (
              <div className="space-y-4">
                {[1, 2, 3].map(i => (
                  <LoadingSkeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            ) : recentInvestigations.length > 0 ? (
              <div className="space-y-4">
                {recentInvestigations.map((investigation) => (
                  <div key={investigation.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                    <div className="flex items-center gap-4">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <Search className="h-4 w-4 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium">{investigation.target}</p>
                        <p className="text-sm text-gray-600 capitalize">
                          {investigation.investigation_type} • {investigation.priority} priority
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge 
                        variant={
                          investigation.status === 'completed' ? 'default' :
                          investigation.status === 'processing' ? 'secondary' :
                          investigation.status === 'failed' ? 'destructive' : 'outline'
                        }
                      >
                        {investigation.status}
                      </Badge>
                      <p className="text-sm text-gray-500">
                        {new Date(investigation.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No investigations yet</p>
                <p className="text-sm text-gray-500 mb-4">Start your first scan to protect yourself from scams</p>
                <Button onClick={() => setShowInvestigationModal(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Start Investigation
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Protection Tips */}
        <Card>
          <CardHeader>
            <CardTitle>Protection Tips</CardTitle>
            <CardDescription>Stay safe with these security recommendations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                {
                  icon: Shield,
                  title: "Verify Email Senders",
                  description: "Always check sender authenticity before clicking links or downloading attachments."
                },
                {
                  icon: AlertTriangle,
                  title: "Suspicious Phone Calls",
                  description: "Be wary of unsolicited calls asking for personal information or urgent payments."
                },
                {
                  icon: TrendingUp,
                  title: "Monitor Your Accounts",
                  description: "Regularly check your financial accounts for unauthorized transactions."
                }
              ].map((tip, index) => (
                <div key={index} className="p-4 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg border-l-4 border-blue-600">
                  <tip.icon className="h-6 w-6 text-blue-600 mb-2" />
                  <h4 className="font-semibold text-gray-900 mb-1">{tip.title}</h4>
                  <p className="text-sm text-gray-600">{tip.description}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Investigation Modal */}
      <InvestigationModal 
        open={showInvestigationModal}
        onOpenChange={setShowInvestigationModal}
      />
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <LoadingSkeleton className="h-48 w-full mb-8" />
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {[1, 2, 3].map(i => (
            <LoadingSkeleton key={i} className="h-32 w-full" />
          ))}
        </div>
        <LoadingSkeleton className="h-64 w-full" />
      </div>
    </div>
  );
}

