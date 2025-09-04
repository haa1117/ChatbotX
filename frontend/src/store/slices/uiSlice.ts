import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  loading: boolean;
  notifications: Array<{
    id: string;
    type: 'success' | 'error' | 'warning' | 'info';
    message: string;
    timestamp: Date;
  }>;
  modals: {
    settingsOpen: boolean;
    helpOpen: boolean;
    feedbackOpen: boolean;
  };
  chatSettings: {
    soundEnabled: boolean;
    notificationsEnabled: boolean;
    autoScroll: boolean;
    compactMode: boolean;
  };
}

const initialState: UIState = {
  theme: 'light',
  sidebarOpen: false,
  loading: false,
  notifications: [],
  modals: {
    settingsOpen: false,
    helpOpen: false,
    feedbackOpen: false,
  },
  chatSettings: {
    soundEnabled: true,
    notificationsEnabled: true,
    autoScroll: true,
    compactMode: false,
  },
};

export const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    addNotification: (state, action: PayloadAction<Omit<UIState['notifications'][0], 'id' | 'timestamp'>>) => {
      const notification = {
        ...action.payload,
        id: Math.random().toString(36),
        timestamp: new Date(),
      };
      state.notifications.push(notification);
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(n => n.id !== action.payload);
    },
    clearNotifications: (state) => {
      state.notifications = [];
    },
    setModalOpen: (state, action: PayloadAction<{ modal: keyof UIState['modals']; open: boolean }>) => {
      state.modals[action.payload.modal] = action.payload.open;
    },
    updateChatSettings: (state, action: PayloadAction<Partial<UIState['chatSettings']>>) => {
      state.chatSettings = { ...state.chatSettings, ...action.payload };
    },
  },
});

export const {
  setTheme,
  toggleSidebar,
  setSidebarOpen,
  setLoading,
  addNotification,
  removeNotification,
  clearNotifications,
  setModalOpen,
  updateChatSettings,
} = uiSlice.actions;

export default uiSlice.reducer; 