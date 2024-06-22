import React, { useState, useEffect } from 'react';
import { checkSession, extendSession, getProtected } from '../api';

function Dashboard() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const response = await checkSession();
        setMessage(response.data.msg);
      } catch (error) {
        setMessage('No active session');
      }
    };

    fetchSession();
  }, []);

  const handleExtendSession = async () => {
    try {
      await extendSession();
      setMessage('Session extended');
    } catch (error) {
      setMessage('Failed to extend session');
    }
  };

  const handleProtectedRequest = async () => {
    try {
      const response = await getProtected();
      setMessage(response.data.msg);
    } catch (error) {
      setMessage('Protected request failed');
    }
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <p>{message}</p>
      <button onClick={handleExtendSession}>Extend Session</button>
      <button onClick={handleProtectedRequest}>Protected Request</button>
    </div>
  );
}

export default Dashboard;
