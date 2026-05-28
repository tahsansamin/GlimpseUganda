import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://glimpseuganda-production.up.railway.app'
});

export default apiClient;