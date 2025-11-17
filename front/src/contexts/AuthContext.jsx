import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser && storedUser !== 'undefined' && storedUser !== 'null') {
      try {
        return JSON.parse(storedUser);
      } catch (error) {
        console.error('Error parsing stored user on initial state:', error);
        // Clear corrupted data
        localStorage.removeItem('user');
        return null;
      }
    }
    return null;
  });
  const [token, setToken] = useState(() => {
    const storedToken = localStorage.getItem('token');
    // Check for 'undefined' string specifically
    if (storedToken === 'undefined' || storedToken === 'null') {
      localStorage.removeItem('token');
      return null;
    }
    return storedToken || null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if token exists on initial load
    const storedToken = localStorage.getItem('token');
    if (storedToken && storedToken !== 'undefined' && storedToken !== 'null') {
      setToken(storedToken);
      const storedUser = localStorage.getItem('user');
      if (storedUser && storedUser !== 'undefined' && storedUser !== 'null') {
        try {
          setUser(JSON.parse(storedUser));
        } catch (error) {
          console.error('Error parsing stored user:', error);
          // Clear corrupted data
          localStorage.removeItem('user');
        }
      }
    }
    setLoading(false);
  }, []);

  const login = (userData, authToken) => {
    // Validate that the token is not 'undefined' or 'null' string
    if (authToken === 'undefined' || authToken === 'null' || !authToken) {
      console.error('Invalid token received:', authToken);
      return;
    }
    setUser(userData);
    setToken(authToken);
    localStorage.setItem('token', authToken);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const registerAndLogin = (userData, authToken) => {
    // Validate that the token is not 'undefined' or 'null' string
    if (authToken === 'undefined' || authToken === 'null' || !authToken) {
      console.error('Invalid token received:', authToken);
      return;
    }
    setUser(userData);
    setToken(authToken);
    localStorage.setItem('token', authToken);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const value = {
    user,
    token,
    login,
    logout,
    registerAndLogin,
    isAuthenticated: !!token,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};