import { useAuth } from '../../contexts/AuthContext';
import { useAdminDashboard } from '../../hooks/useDashboard';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { LoadingSpinner, LoadingSkeleton } from '../ui/LoadingSpinner';
import { 
  Shield, 
  Users, 
  FileText, 
  DollarSign,
  TrendingUp,
  TrendingDown,
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react';

export function AdminDashboard() {
  const { user, logout } = useAuth();
  const { adminData, loading, error } = useAdminDashboard();

  const handleLogout = async () => {
    await logout();
  };

  if (loading) {
    return <AdminDashboardSkeleton />;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="w-96">
          <CardHeader>
            <CardTitle className="text-red-600">Error Loading Dashboard</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-4">{error.message || 'Failed to load admin dashboard'}</p>
            <Button onClick={() => window.location.reload()}>Retry</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const stats = adminData?.stats || {
    totalRevenue: 0,
    totalUsers: 0,
    totalReports: 0,
    accuracyRate: 0,
    revenueChange: 0,
    usersChange: 0,
    reportsChange: 0,
    accuracyChange: 0
  };

  const chartData = adminData?.chartData || {
    revenue: [],
    users: [],
    reports: []
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 w-64 h-full bg-gradient-to-b from-blue-600 to-purple-600 text-white z-50">
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-2">
            <Shield className="h-8 w-8" />
            <span className="text-xl font-bold">ScamShield AI</span>
          </div>
        </div>
        
        <nav className="p-4 space-y-2">
          <NavItem icon={Activity} label="Dashboard" active />
          <NavItem icon={Users} label="Users" />
          <NavItem icon={FileText} label="Reports" />
          <NavItem icon={AlertTriangle} label="Investigations" />
          <NavItem icon={DollarSign} label="Payments" />
          <NavItem icon={Shield} label="Security" />
        </nav>
      </div>

      {/* Main Content */}
      <div className="ml-64">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white font-semibold text-sm">
                  {user?.user_metadata?.full_name?.[0] || 'A'}
                </div>
                <span className="text-sm font-medium text-gray-700">
                  {user?.user_metadata?.full_name || 'Admin'}
                </span>
              </div>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </div>
        </header>

        <div className="p-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total Revenue"
              value={`$${(stats.totalRevenue || 0).toLocaleString()}`}
              change={stats.revenueChange || 0}
              icon={DollarSign}
              iconColor="text-green-600"
              iconBg="bg-green-100"
            />
            <StatCard
              title="Total Users"
              value={(stats.totalUsers || 0).toLocaleString()}
              change={stats.usersChange || 0}
              icon={Users}
              iconColor="text-blue-600"
              iconBg="bg-blue-100"
            />
            <StatCard
              title="Total Reports"
              value={(stats.totalReports || 0).toLocaleString()}
              change={stats.reportsChange || 0}
              icon={FileText}
              iconColor="text-yellow-600"
              iconBg="bg-yellow-100"
            />
            <StatCard
              title="Accuracy Rate"
              value={`${(stats.accuracyRate || 0).toFixed(1)}%`}
              change={stats.accuracyChange || 0}
              icon={Shield}
              iconColor="text-purple-600"
              iconBg="bg-purple-100"
            />
          </div>

          {/* Charts and Tables */}
          <div className="grid lg:grid-cols-3 gap-6 mb-8">
            {/* Revenue Chart Placeholder */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <div>
                    <CardTitle>Revenue Trends</CardTitle>
                    <CardDescription>Monthly revenue over the last 12 months</CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">7D</Button>
                    <Button variant="outline" size="sm">30D</Button>
                    <Button variant="outline" size="sm" className="bg-blue-600 text-white">12M</Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
                  <p className="text-gray-500">Chart visualization would go here</p>
                </div>
              </CardContent>
            </Card>

            {/* Activity Feed */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Latest system activities</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { type: 'user', message: 'New user registered', time: '2 min ago', icon: Users, color: 'text-blue-600' },
                    { type: 'report', message: 'Investigation completed', time: '5 min ago', icon: FileText, color: 'text-green-600' },
                    { type: 'payment', message: 'Payment received', time: '10 min ago', icon: DollarSign, color: 'text-green-600' },
                    { type: 'alert', message: 'High-risk detection', time: '15 min ago', icon: AlertTriangle, color: 'text-red-600' }
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center gap-3">
                      <div className={`p-2 rounded-full bg-gray-100`}>
                        <activity.icon className={`h-4 w-4 ${activity.color}`} />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">{activity.message}</p>
                        <p className="text-xs text-gray-500">{activity.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Reports Table */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Recent Reports</CardTitle>
                  <CardDescription>Latest investigation reports from users</CardDescription>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">Export</Button>
                  <Button variant="outline" size="sm">Filter</Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-600">ID</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Target</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Type</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Status</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">User</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Date</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {[
                      { id: 'INV-001', target: 'suspicious@example.com', type: 'Email', status: 'completed', user: 'john@example.com', date: '2024-01-15' },
                      { id: 'INV-002', target: '+1-555-123-4567', type: 'Phone', status: 'processing', user: 'jane@example.com', date: '2024-01-15' },
                      { id: 'INV-003', target: 'scam-site.com', type: 'Domain', status: 'failed', user: 'bob@example.com', date: '2024-01-14' },
                      { id: 'INV-004', target: '192.168.1.100', type: 'IP', status: 'pending', user: 'alice@example.com', date: '2024-01-14' }
                    ].map((report) => (
                      <tr key={report.id} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4 font-mono text-sm">{report.id}</td>
                        <td className="py-3 px-4 font-medium">{report.target}</td>
                        <td className="py-3 px-4 text-sm">{report.type}</td>
                        <td className="py-3 px-4">
                          <Badge 
                            variant={
                              report.status === 'completed' ? 'default' :
                              report.status === 'processing' ? 'secondary' :
                              report.status === 'failed' ? 'destructive' : 'outline'
                            }
                          >
                            {report.status}
                          </Badge>
                        </td>
                        <td className="py-3 px-4 text-sm">{report.user}</td>
                        <td className="py-3 px-4 text-sm">{report.date}</td>
                        <td className="py-3 px-4">
                          <Button variant="ghost" size="sm">View</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

function NavItem({ icon: Icon, label, active = false }) {
  return (
    <div className={`flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
      active ? 'bg-white/20 text-white' : 'text-white/80 hover:bg-white/10 hover:text-white'
    }`}>
      <Icon className="h-5 w-5" />
      <span className="font-medium">{label}</span>
    </div>
  );
}

function StatCard({ title, value, change, icon: Icon, iconColor, iconBg }) {
  const isPositive = change >= 0;
  
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex justify-between items-center mb-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <div className={`p-2 rounded-lg ${iconBg}`}>
            <Icon className={`h-5 w-5 ${iconColor}`} />
          </div>
        </div>
        <div className="space-y-1">
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          <div className="flex items-center gap-1">
            {isPositive ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600" />
            )}
            <span className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {isPositive ? '+' : ''}{change.toFixed(1)}%
            </span>
            <span className="text-sm text-gray-500">vs last month</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function AdminDashboardSkeleton() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="ml-64 p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[1, 2, 3, 4].map(i => (
            <LoadingSkeleton key={i} className="h-32 w-full" />
          ))}
        </div>
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <LoadingSkeleton className="h-80 lg:col-span-2" />
          <LoadingSkeleton className="h-80" />
        </div>
        <LoadingSkeleton className="h-64 w-full" />
      </div>
    </div>
  );
}

