const API_PORT = '3000';

const API_ROOT = `http://106.14.227.202:${API_PORT}`;

const DEFAULT_ICE_SERVER = {
  url: 'turn:106.14.227.202:3478',
  credential: 'interview',
  username: 'interview',
};

module.exports = { API_PORT, API_ROOT, DEFAULT_ICE_SERVER };
