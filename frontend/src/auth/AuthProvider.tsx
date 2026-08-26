import React, { createContext, useContext, useState } from 'react';

export interface UserProfile {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'controller' | 'approver' | 'ap_clerk' | 'viewer';
  organizationId: string;
  organizationName: string;
}

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  login: (email: string, role?: UserProfile['role']) => void;
  logout: () => void;
}

const defaultUser: UserProfile = {
  id: 'usr-101',
  email: 'alex.vance@finguard.com',
  name: 'Alex Vance',
  role: 'controller',
  organizationId: 'org-acme-01',
  organizationName: 'Acme Global Corp',
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(defaultUser);

  const login = (email: string, role: UserProfile['role'] = 'controller') => {
    setUser({
      id: 'usr-' + Math.random().toString(36).substring(2, 7),
      email,
      name: email.split('@')[0].replace('.', ' ').toUpperCase(),
      role,
      organizationId: 'org-acme-01',
      organizationName: 'Acme Global Corp',
    });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
