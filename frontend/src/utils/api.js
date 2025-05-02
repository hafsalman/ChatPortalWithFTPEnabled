import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // Your FastAPI backend URL

export const loginUser = async (username, password) => {
  return await axios.post(`${API_URL}/login`, { username, password });
};

export const registerUser = async (full_name, username, email, password, phone_number, profile_picture) => {
  return await axios.post(`${API_URL}/register`, {
    full_name,
    username,
    email,
    password,
    phone_number,
    profile_picture,
  });
};

export const sendMessage = async (sender, receiver, message) => {
  return await axios.post(`${API_URL}/send`, { sender, receiver, message });
};

export const getMessages = async (user, since) => {
  return await axios.get(`${API_URL}/messages`, { params: { user, since } });
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return await axios.post(`${API_URL}/uploadfile/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const downloadFile = async (filename) => {
  return await axios.get(`${API_URL}/downloadfile/${filename}`);
};