const API_BASE_URL = 'http://127.0.0.1:8000/api';

async function apiRequest(endpoint, method = 'GET', data = null, isFormData = false) {
  const token = localStorage.getItem('token');
  const headers = {};

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const options = { method, headers };

  if (data) {
    if (isFormData) {
      options.body = data;
    } else {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(data);
    }
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const result = await response.json();

    if (!response.ok) {
      if (response.status === 401 && !endpoint.includes('/auth/login')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
      }
      throw new Error(result.detail || 'API request failed');
    }

    return result;
  } catch (error) {
    console.error(`[API Error] ${endpoint}:`, error);
    throw error;
  }
}
