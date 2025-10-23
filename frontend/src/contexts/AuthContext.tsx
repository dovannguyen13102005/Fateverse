import React, { createContext, useContext, useEffect, useState } from 'react';
import { authAPI } from '../utils/api';

interface User {
  id: string;
  name: string;
  email: string;
  picture?: string;
  birth_date?: string;
  theme_preference?: string;
  created_at?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  loginWithGoogle: (credential: string) => Promise<void>;
  loginWithEmail: (email: string, password: string) => Promise<void>;
  registerWithEmail: (data: { email: string; password: string; name: string; birth_date?: string; gender?: string }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in on mount
    const checkAuthStatus = async () => {
      const token = localStorage.getItem('authToken');
      const userInfo = localStorage.getItem('userInfo');
      
      if (token && userInfo) {
        try {
          const userData = JSON.parse(userInfo);
          setUser(userData);
        } catch (error) {
          console.error('Error parsing user info:', error);
          localStorage.removeItem('authToken');
          localStorage.removeItem('userInfo');
        }
      }
      
      setIsLoading(false);
    };

    checkAuthStatus();
  }, []);

  const loginWithGoogle = async (credential: string) => {
    try {
      setIsLoading(true);
      const response = await authAPI.googleLogin(credential);
      
      const { user: userData, token } = response.data;
      
      // Save to localStorage
      localStorage.setItem('authToken', token);
      localStorage.setItem('userInfo', JSON.stringify(userData));
      
      setUser(userData);
    } catch (error: any) {
      console.error('Google login failed:', error);
      throw new Error(error.response?.data?.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const loginWithEmail = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      const response = await authAPI.emailLogin(email, password);
      
      const { user: userData, token } = response.data;
      
      // Save to localStorage
      localStorage.setItem('authToken', token);
      localStorage.setItem('userInfo', JSON.stringify(userData));
      
      setUser(userData);
    } catch (error: any) {
      console.error('Email login failed:', error);
      throw new Error(error.response?.data?.detail || 'Đăng nhập thất bại');
    } finally {
      setIsLoading(false);
    }
  };

  const registerWithEmail = async (data: { 
    email: string; 
    password: string; 
    name: string; 
    birth_date?: string; 
    gender?: string 
  }) => {
    try {
      setIsLoading(true);
      const response = await authAPI.emailRegister(data);
      
      const { user: userData, token } = response.data;
      
      // Save to localStorage
      localStorage.setItem('authToken', token);
      localStorage.setItem('userInfo', JSON.stringify(userData));
      
      setUser(userData);
    } catch (error: any) {
      console.error('Email registration failed:', error);
      throw new Error(error.response?.data?.detail || 'Đăng ký thất bại');
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userInfo');
    setUser(null);
    
    // Call logout API
    authAPI.logout().catch(console.error);
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    loginWithGoogle,
    loginWithEmail,
    registerWithEmail,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};