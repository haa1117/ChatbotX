import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ConversationMetric {
  date: string;
  totalConversations: number;
  uniqueUsers: number;
  averageResponseTime: number;
  satisfactionScore: number;
}

interface IntentMetric {
  intent: string;
  count: number;
  accuracy: number;
}

interface UserEngagementMetric {
  date: string;
  activeUsers: number;
  sessionDuration: number;
  messagesPerSession: number;
}

interface AnalyticsState {
  conversationMetrics: ConversationMetric[];
  intentMetrics: IntentMetric[];
  userEngagementMetrics: UserEngagementMetric[];
  totalConversations: number;
  totalUsers: number;
  averageSatisfaction: number;
  mostCommonIntents: string[];
  isLoading: boolean;
  error: string | null;
  dateRange: {
    start: string;
    end: string;
  };
}

const initialState: AnalyticsState = {
  conversationMetrics: [],
  intentMetrics: [],
  userEngagementMetrics: [],
  totalConversations: 0,
  totalUsers: 0,
  averageSatisfaction: 0,
  mostCommonIntents: [],
  isLoading: false,
  error: null,
  dateRange: {
    start: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0],
  },
};

export const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    setConversationMetrics: (state, action: PayloadAction<ConversationMetric[]>) => {
      state.conversationMetrics = action.payload;
    },
    setIntentMetrics: (state, action: PayloadAction<IntentMetric[]>) => {
      state.intentMetrics = action.payload;
    },
    setUserEngagementMetrics: (state, action: PayloadAction<UserEngagementMetric[]>) => {
      state.userEngagementMetrics = action.payload;
    },
    setTotalConversations: (state, action: PayloadAction<number>) => {
      state.totalConversations = action.payload;
    },
    setTotalUsers: (state, action: PayloadAction<number>) => {
      state.totalUsers = action.payload;
    },
    setAverageSatisfaction: (state, action: PayloadAction<number>) => {
      state.averageSatisfaction = action.payload;
    },
    setMostCommonIntents: (state, action: PayloadAction<string[]>) => {
      state.mostCommonIntents = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
    setDateRange: (state, action: PayloadAction<{ start: string; end: string }>) => {
      state.dateRange = action.payload;
    },
    clearAnalytics: (state) => {
      state.conversationMetrics = [];
      state.intentMetrics = [];
      state.userEngagementMetrics = [];
      state.totalConversations = 0;
      state.totalUsers = 0;
      state.averageSatisfaction = 0;
      state.mostCommonIntents = [];
      state.error = null;
    },
  },
});

export const {
  setConversationMetrics,
  setIntentMetrics,
  setUserEngagementMetrics,
  setTotalConversations,
  setTotalUsers,
  setAverageSatisfaction,
  setMostCommonIntents,
  setLoading,
  setError,
  setDateRange,
  clearAnalytics,
} = analyticsSlice.actions;

export default analyticsSlice.reducer; 