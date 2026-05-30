import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKENDURL
});

export default apiClient;


