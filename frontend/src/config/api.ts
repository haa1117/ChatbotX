export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8082',
  WS_URL: process.env.REACT_APP_WS_URL || 'ws://localhost:8082',
  ENDPOINTS: {
    HEALTH: '/health',
    CHAT: '/api/v1/chat/message',
    COURSES: '/api/v1/courses',
    ANALYTICS: '/api/v1/analytics/dashboard',
    CONTACT: '/api/v1/contact',
    FAQ: '/api/v1/faq',
  },
  TIMEOUT: 10000,
};

export default API_CONFIG; 