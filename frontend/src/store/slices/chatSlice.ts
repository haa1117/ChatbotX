import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  buttons?: Array<{ title: string; payload: string }>;
  quick_replies?: Array<{ title: string; payload: string }>;
  suggestions?: string[];
  metadata?: any;
}

interface ChatState {
  messages: Message[];
  isTyping: boolean;
  isConnected: boolean;
  currentLanguage: string;
  sessionId: string | null;
  conversationHistory: Message[];
}

const initialState: ChatState = {
  messages: [],
  isTyping: false,
  isConnected: false,
  currentLanguage: 'en',
  sessionId: null,
  conversationHistory: [],
};

export const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<Message>) => {
      state.messages.push(action.payload);
      state.conversationHistory.push(action.payload);
    },
    setTyping: (state, action: PayloadAction<boolean>) => {
      state.isTyping = action.payload;
    },
    setConnected: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
    },
    setLanguage: (state, action: PayloadAction<string>) => {
      state.currentLanguage = action.payload;
    },
    setSessionId: (state, action: PayloadAction<string>) => {
      state.sessionId = action.payload;
    },
    clearMessages: (state) => {
      state.messages = [];
    },
    clearHistory: (state) => {
      state.conversationHistory = [];
    },
  },
});

export const {
  addMessage,
  setTyping,
  setConnected,
  setLanguage,
  setSessionId,
  clearMessages,
  clearHistory,
} = chatSlice.actions;

export default chatSlice.reducer; 