import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { PublicLayout } from './components/Layout/PublicLayout';
import { HomePage } from './pages/HomePage';
import { FeaturesPage } from './pages/public/FeaturesPage';
import { SecurityPage } from './pages/public/SecurityPage';
import { IntegrationsPage } from './pages/public/IntegrationsPage';
import { PricingPage } from './pages/public/PricingPage';
import { LoginPage } from './pages/LoginPage';
import { LogoutPage } from './pages/LogoutPage';
import { AppLayout } from './components/Layout/AppLayout';
import { DashboardPage } from './pages/DashboardPage';
import { CapturePage } from './pages/CapturePage';
import { InvoicesPage } from './pages/InvoicesPage';
import { ReviewStudioPage } from './pages/ReviewStudioPage';
import { ExceptionsPage } from './pages/ExceptionsPage';
import { ApprovalsPage } from './pages/ApprovalsPage';
import { VendorsPage } from './pages/VendorsPage';
import { ReportsPage } from './pages/ReportsPage';
import { AuditPage } from './pages/AuditPage';
import { SettingsPage } from './pages/SettingsPage';
import { NotFoundPage } from './pages/NotFoundPage';
import './App.css';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Marketing Landing & Info Pages */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/features" element={<FeaturesPage />} />
          <Route path="/security" element={<SecurityPage />} />
          <Route path="/integrations" element={<IntegrationsPage />} />
          <Route path="/pricing" element={<PricingPage />} />
        </Route>

        {/* Standalone Auth Pages */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<LoginPage />} />
        <Route path="/logout" element={<LogoutPage />} />

        {/* Authenticated Application Workspace */}
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/capture" element={<CapturePage />} />
          <Route path="/invoices" element={<InvoicesPage />} />
          <Route path="/invoices/:id/review" element={<ReviewStudioPage />} />
          <Route path="/exceptions" element={<ExceptionsPage />} />
          <Route path="/approvals" element={<ApprovalsPage />} />
          <Route path="/vendors" element={<VendorsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/audit" element={<AuditPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
