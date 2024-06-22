import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/auth',
  withCredentials: true,
});

export const register = (data) => api.post('/register', data);
export const login = (data) => api.post('/login', data);
export const checkSession = () => api.get('/check_session');
export const extendSession = () => api.post('/extend_session');
export const getProtected = () => api.get('/protected', {
  headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
});
