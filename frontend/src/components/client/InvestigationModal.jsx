import { useState } from 'react';
import { useInvestigations } from '../../hooks/useInvestigations';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '../ui/dialog';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Alert, AlertDescription } from '../ui/alert';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import { Search, Mail, Phone, Globe, MapPin, Users } from 'lucide-react';

const investigationTypes = [
  { value: 'email', label: 'Email Address', icon: Mail, description: 'Verify email sender authenticity' },
  { value: 'phone', label: 'Phone Number', icon: Phone, description: 'Check phone number legitimacy' },
  { value: 'domain', label: 'Website/Domain', icon: Globe, description: 'Analyze website safety' },
  { value: 'ip', label: 'IP Address', icon: MapPin, description: 'Investigate IP location and reputation' },
  { value: 'social_media', label: 'Social Media', icon: Users, description: 'Verify social media profiles' }
];

const priorities = [
  { value: 'low', label: 'Low Priority', color: 'text-gray-600' },
  { value: 'medium', label: 'Medium Priority', color: 'text-yellow-600' },
  { value: 'high', label: 'High Priority', color: 'text-orange-600' },
  { value: 'urgent', label: 'Urgent', color: 'text-red-600' }
];

export function InvestigationModal({ open, onOpenChange }) {
  const [formData, setFormData] = useState({
    target: '',
    type: '',
    priority: 'medium'
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const { createInvestigation } = useInvestigations();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    if (!formData.target.trim()) {
      setError('Please enter a target to investigate');
      setIsSubmitting(false);
      return;
    }

    if (!formData.type) {
      setError('Please select an investigation type');
      setIsSubmitting(false);
      return;
    }

    const result = await createInvestigation(formData);
    
    if (result.success) {
      // Reset form and close modal
      setFormData({ target: '', type: '', priority: 'medium' });
      onOpenChange(false);
    } else {
      setError(result.error || 'Failed to create investigation');
    }
    
    setIsSubmitting(false);
  };

  const handleClose = () => {
    if (!isSubmitting) {
      setFormData({ target: '', type: '', priority: 'medium' });
      setError('');
      onOpenChange(false);
    }
  };

  const selectedType = investigationTypes.find(type => type.value === formData.type);

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Search className="h-5 w-5 text-blue-600" />
            New Investigation
          </DialogTitle>
          <DialogDescription>
            Start a new scam detection investigation. Our AI will analyze your target and provide a comprehensive report.
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          
          {/* Investigation Type Selection */}
          <div className="space-y-3">
            <Label>Investigation Type</Label>
            <div className="grid grid-cols-1 gap-2">
              {investigationTypes.map((type) => {
                const Icon = type.icon;
                return (
                  <div
                    key={type.value}
                    className={`p-3 border rounded-lg cursor-pointer transition-all ${
                      formData.type === type.value
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setFormData(prev => ({ ...prev, type: type.value }))}
                  >
                    <div className="flex items-center gap-3">
                      <Icon className={`h-5 w-5 ${
                        formData.type === type.value ? 'text-blue-600' : 'text-gray-400'
                      }`} />
                      <div>
                        <p className={`font-medium ${
                          formData.type === type.value ? 'text-blue-900' : 'text-gray-900'
                        }`}>
                          {type.label}
                        </p>
                        <p className={`text-sm ${
                          formData.type === type.value ? 'text-blue-600' : 'text-gray-500'
                        }`}>
                          {type.description}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Target Input */}
          <div className="space-y-2">
            <Label htmlFor="target">
              {selectedType ? `${selectedType.label} to Investigate` : 'Target to Investigate'}
            </Label>
            <div className="relative">
              {selectedType && (
                <selectedType.icon className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              )}
              <Input
                id="target"
                type="text"
                placeholder={
                  formData.type === 'email' ? 'Enter email address (e.g., suspicious@example.com)' :
                  formData.type === 'phone' ? 'Enter phone number (e.g., +1-555-123-4567)' :
                  formData.type === 'domain' ? 'Enter website URL (e.g., suspicious-site.com)' :
                  formData.type === 'ip' ? 'Enter IP address (e.g., 192.168.1.1)' :
                  formData.type === 'social_media' ? 'Enter profile URL or username' :
                  'Enter target to investigate'
                }
                value={formData.target}
                onChange={(e) => setFormData(prev => ({ ...prev, target: e.target.value }))}
                className={selectedType ? 'pl-10' : ''}
                required
                disabled={isSubmitting}
              />
            </div>
          </div>

          {/* Priority Selection */}
          <div className="space-y-2">
            <Label>Priority Level</Label>
            <Select 
              value={formData.priority} 
              onValueChange={(value) => setFormData(prev => ({ ...prev, priority: value }))}
              disabled={isSubmitting}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {priorities.map((priority) => (
                  <SelectItem key={priority.value} value={priority.value}>
                    <span className={priority.color}>{priority.label}</span>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <p className="text-sm text-gray-500">
              Higher priority investigations are processed faster but may cost more credits.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isSubmitting}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting || !formData.target.trim() || !formData.type}
              className="flex-1"
            >
              {isSubmitting ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Starting Investigation...
                </>
              ) : (
                <>
                  <Search className="h-4 w-4 mr-2" />
                  Start Investigation
                </>
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}

