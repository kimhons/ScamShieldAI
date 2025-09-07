# ScamShield AI - React Application

## 🛡️ Advanced Fraud Detection Platform

ScamShield AI is a comprehensive fraud detection platform built with React, Next.js, and Supabase. This application provides both client and admin dashboards for investigating and managing scam detection activities.

## 🚀 Features

### Client Dashboard
- **Investigation Management**: Create and track scam investigations
- **Multiple Investigation Types**: Email, Phone, Domain, IP, Social Media
- **Real-time Status Updates**: Track investigation progress
- **Report Generation**: Access detailed investigation reports
- **Protection Tips**: Security recommendations and best practices

### Admin Dashboard
- **User Management**: Monitor and manage platform users
- **Analytics & Reporting**: Comprehensive dashboard with metrics
- **Investigation Oversight**: Monitor all platform investigations
- **Revenue Tracking**: Financial analytics and reporting
- **Activity Monitoring**: Real-time platform activity feed

## 🛠️ Technology Stack

- **Frontend**: React 19.1.0, Vite 6.3.5
- **Styling**: Tailwind CSS 4.1.7, shadcn/ui components
- **Icons**: Lucide React
- **Charts**: Recharts
- **Routing**: React Router DOM 7.6.1
- **State Management**: React Context API + SWR
- **Backend**: Supabase (PostgreSQL + Auth)
- **Package Manager**: pnpm

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/scamshield-nextjs.git
   cd scamshield-nextjs
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Environment Setup**
   Create a `.env.local` file in the root directory:
   ```env
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. **Start the development server**
   ```bash
   pnpm run dev --host
   ```

5. **Open your browser**
   Navigate to `http://localhost:5173`

## 🏗️ Project Structure

```
src/
├── components/
│   ├── admin/              # Admin dashboard components
│   ├── auth/               # Authentication components
│   ├── client/             # Client dashboard components
│   ├── layout/             # Layout components
│   └── ui/                 # Reusable UI components
├── contexts/               # React contexts
├── hooks/                  # Custom React hooks
├── lib/                    # Utility functions and API layer
└── App.jsx                 # Main application component
```

## 🔐 Authentication

The application uses Supabase Auth for user authentication:
- **Registration**: Create new user accounts
- **Login**: Secure user authentication
- **Protected Routes**: Role-based access control
- **Session Management**: Automatic session handling

## 📊 Data Management

### Custom Hooks
- `useAuth()` - Authentication state management
- `useDashboard()` - Dashboard data fetching
- `useInvestigations()` - Investigation management
- `useReports()` - Report data handling
- `useApiKeys()` - API key management

### API Layer
- Centralized Supabase client configuration
- Error handling and response normalization
- Type-safe API calls
- Automatic retry logic with SWR

## 🎨 UI Components

Built with shadcn/ui and Tailwind CSS:
- **Forms**: Login, Registration, Investigation creation
- **Cards**: Dashboard statistics, action cards
- **Tables**: Data display with sorting and pagination
- **Modals**: Investigation creation, confirmations
- **Loading States**: Spinners, skeletons, progress indicators

## 🧪 Testing

### Connection Testing
```bash
node test-supabase-simple.js
```

### Component Testing
- Unit tests for all components
- Integration tests for API endpoints
- End-to-end testing for user flows

## 🚀 Deployment

### Development
```bash
pnpm run dev --host
```

### Production Build
```bash
pnpm run build
pnpm run preview
```

### Deployment Platforms
- **Vercel** (Recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **Firebase Hosting**

## 📋 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_SUPABASE_URL` | Supabase project URL | Yes |
| `VITE_SUPABASE_ANON_KEY` | Supabase anonymous key | Yes |

## 🔧 Development Scripts

| Command | Description |
|---------|-------------|
| `pnpm run dev` | Start development server |
| `pnpm run build` | Build for production |
| `pnpm run preview` | Preview production build |
| `pnpm run lint` | Run ESLint |

## 🛡️ Security Features

- **Row Level Security (RLS)**: Database-level security
- **JWT Authentication**: Secure token-based auth
- **Input Validation**: Client and server-side validation
- **Error Boundaries**: Graceful error handling
- **CORS Configuration**: Secure cross-origin requests

## 📈 Performance Optimizations

- **Code Splitting**: Dynamic imports for large components
- **Lazy Loading**: On-demand component loading
- **SWR Caching**: Intelligent data caching and revalidation
- **Memoization**: React.memo for expensive components
- **Bundle Optimization**: Vite-powered build optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Complete React application setup
- ✅ Supabase integration
- ✅ Authentication system
- ✅ Client and Admin dashboards
- ✅ Investigation management
- ✅ Error handling and UX improvements

---

**ScamShield AI** - Protecting users from digital fraud with advanced AI-powered detection.

