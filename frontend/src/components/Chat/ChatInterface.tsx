import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Chip,
  Avatar,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Button,
  CircularProgress,
  Tooltip,
  Badge,
} from '@mui/material';
import {
  Send as SendIcon,
  Mic as MicIcon,
  AttachFile as AttachFileIcon,
  EmojiEmotions as EmojiIcon,
  Settings as SettingsIcon,
  Chat as ChatIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  VolumeUp as VolumeUpIcon,
  Translate as TranslateIcon,
  Feedback as FeedbackIcon,
  Close as CloseIcon,
  Fullscreen as FullscreenIcon,
  FullscreenExit as FullscreenExitIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { io, Socket } from 'socket.io-client';
import toast from 'react-hot-toast';

// Types
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  typing?: boolean;
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
  isFullscreen: boolean;
  showSettings: boolean;
}

const ChatInterface: React.FC = () => {
  // State management
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isTyping: false,
    isConnected: false,
    currentLanguage: 'en',
    isFullscreen: false,
    showSettings: false,
  });
  
  const [inputMessage, setInputMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [clientId] = useState(() => Math.random().toString(36).substr(2, 9));
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const socketRef = useRef<Socket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  
  // Initialize WebSocket connection
  useEffect(() => {
    const initializeConnection = () => {
      socketRef.current = io('ws://localhost:8080', {
        transports: ['websocket'],
      });
      
      socketRef.current.on('connect', () => {
        setChatState(prev => ({ ...prev, isConnected: true }));
        toast.success('Connected to ChatBotX!');
        
        // Send welcome message
        addMessage({
          id: Math.random().toString(36),
          text: '👋 Welcome to ChatBotX! I\'m your AI Education Assistant. How can I help you today?',
          sender: 'bot',
          timestamp: new Date(),
          quick_replies: [
            { title: 'Browse Courses', payload: '/courses' },
            { title: 'Enrollment Help', payload: '/enrollment' },
            { title: 'FAQ', payload: '/faq' },
            { title: 'Contact Support', payload: '/support' },
          ],
        });
      });
      
      socketRef.current.on('disconnect', () => {
        setChatState(prev => ({ ...prev, isConnected: false }));
        toast.error('Connection lost. Reconnecting...');
      });
      
      socketRef.current.on('bot_response', (data: any) => {
        setChatState(prev => ({ ...prev, isTyping: false }));
        
        addMessage({
          id: Math.random().toString(36),
          text: data.text,
          sender: 'bot',
          timestamp: new Date(),
          buttons: data.buttons,
          quick_replies: data.quick_replies,
          suggestions: data.suggestions,
          metadata: data.metadata,
        });
      });
      
      socketRef.current.on('typing', (data: any) => {
        setChatState(prev => ({ ...prev, isTyping: data.is_typing }));
      });
      
      socketRef.current.on('system', (data: any) => {
        if (data.message_type === 'error') {
          toast.error(data.message);
        } else {
          toast.success(data.message);
        }
      });
    };
    
    initializeConnection();
    
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);
  
  // Auto-scroll to bottom
  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages, chatState.isTyping]);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const addMessage = useCallback((message: Message) => {
    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, message],
    }));
  }, []);
  
  const sendMessage = useCallback(async (message: string, payload?: string) => {
    if (!message.trim() || !socketRef.current) return;
    
    // Add user message
    const userMessage: Message = {
      id: Math.random().toString(36),
      text: message,
      sender: 'user',
      timestamp: new Date(),
    };
    
    addMessage(userMessage);
    setInputMessage('');
    setChatState(prev => ({ ...prev, isTyping: true }));
    
    // Send to server
    socketRef.current.emit('message', {
      sender: clientId,
      message: message,
      payload: payload,
      metadata: {
        timestamp: new Date().toISOString(),
        language: chatState.currentLanguage,
      },
    });
  }, [clientId, chatState.currentLanguage, addMessage]);
  
  const handleInputSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };
  
  const handleQuickReply = (title: string, payload: string) => {
    sendMessage(title, payload);
  };
  
  const handleVoiceRecording = () => {
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };
  
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      const audioChunks: BlobPart[] = [];
      mediaRecorderRef.current.addEventListener('dataavailable', (event) => {
        audioChunks.push(event.data);
      });
      
      mediaRecorderRef.current.addEventListener('stop', () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        // Process audio blob (send to speech-to-text service)
        processAudioMessage(audioBlob);
      });
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
      toast.success('Recording started...');
    } catch (error) {
      toast.error('Could not access microphone');
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      toast.success('Recording stopped');
    }
  };
  
  const processAudioMessage = async (audioBlob: Blob) => {
    // Placeholder for speech-to-text processing
    toast.success('Audio message processed');
  };
  
  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = chatState.currentLanguage;
      speechSynthesis.speak(utterance);
    }
  };
  
  const toggleFullscreen = () => {
    setChatState(prev => ({ ...prev, isFullscreen: !prev.isFullscreen }));
  };
  
  const renderMessage = (message: Message) => (
    <motion.div
      key={message.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
          mb: 2,
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            maxWidth: '70%',
            flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
          }}
        >
          <Avatar
            sx={{
              bgcolor: message.sender === 'user' ? 'primary.main' : 'secondary.main',
              mx: 1,
              width: 32,
              height: 32,
            }}
          >
            {message.sender === 'user' ? <PersonIcon /> : <BotIcon />}
          </Avatar>
          
          <Paper
            elevation={2}
            sx={{
              p: 2,
              bgcolor: message.sender === 'user' ? 'primary.light' : 'grey.100',
              color: message.sender === 'user' ? 'white' : 'text.primary',
              borderRadius: 2,
              position: 'relative',
            }}
          >
            <ReactMarkdown
              components={{
                code({ node, className, children, ...props }: any) {
                  const match = /language-(\w+)/.exec(className || '');
                  const inline = !match;
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={tomorrow}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {message.text}
            </ReactMarkdown>
            
            <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                {message.timestamp.toLocaleTimeString()}
              </Typography>
              
              {message.sender === 'bot' && (
                <Tooltip title="Listen">
                  <IconButton
                    size="small"
                    onClick={() => speakText(message.text)}
                    sx={{ opacity: 0.7 }}
                  >
                    <VolumeUpIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              )}
            </Box>
            
            {/* Quick Replies */}
            {message.quick_replies && (
              <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {message.quick_replies.map((reply, index) => (
                  <Chip
                    key={index}
                    label={reply.title}
                    variant="outlined"
                    size="small"
                    clickable
                    onClick={() => handleQuickReply(reply.title, reply.payload)}
                    sx={{
                      bgcolor: 'background.paper',
                      '&:hover': { bgcolor: 'primary.light', color: 'white' },
                    }}
                  />
                ))}
              </Box>
            )}
            
            {/* Action Buttons */}
            {message.buttons && (
              <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 1 }}>
                {message.buttons.map((button, index) => (
                  <Button
                    key={index}
                    variant="outlined"
                    size="small"
                    onClick={() => handleQuickReply(button.title, button.payload)}
                    sx={{ justifyContent: 'flex-start' }}
                  >
                    {button.title}
                  </Button>
                ))}
              </Box>
            )}
          </Paper>
        </Box>
      </Box>
    </motion.div>
  );
  
  const containerSx = chatState.isFullscreen
    ? {
        position: 'fixed' as const,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 9999,
        bgcolor: 'background.default',
      }
    : {
        height: '80vh',
        maxWidth: '800px',
        mx: 'auto',
        mt: 2,
        mb: 2,
      };
  
  return (
    <Box sx={containerSx}>
      <Paper
        elevation={8}
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <Box
          sx={{
            p: 2,
            bgcolor: 'primary.main',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar sx={{ bgcolor: 'secondary.main' }}>
              <ChatIcon />
            </Avatar>
            <Box>
              <Typography variant="h6">ChatBotX</Typography>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>
                <Badge
                  color={chatState.isConnected ? 'success' : 'error'}
                  variant="dot"
                  sx={{ mr: 1 }}
                />
                {chatState.isConnected ? 'Online' : 'Offline'}
              </Typography>
            </Box>
          </Box>
          
          <Box>
            <Tooltip title="Settings">
              <IconButton
                color="inherit"
                onClick={() => setChatState(prev => ({ ...prev, showSettings: true }))}
              >
                <SettingsIcon />
              </IconButton>
            </Tooltip>
            
            <Tooltip title={chatState.isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}>
              <IconButton color="inherit" onClick={toggleFullscreen}>
                {chatState.isFullscreen ? <FullscreenExitIcon /> : <FullscreenIcon />}
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
        
        {/* Messages Area */}
        <Box
          sx={{
            flexGrow: 1,
            overflow: 'auto',
            p: 2,
            bgcolor: 'grey.50',
          }}
        >
          <AnimatePresence>
            {chatState.messages.map(renderMessage)}
          </AnimatePresence>
          
          {/* Typing Indicator */}
          {chatState.isTyping && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
                  <BotIcon />
                </Avatar>
                <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <CircularProgress size={8} />
                    <CircularProgress size={8} sx={{ animationDelay: '0.2s' }} />
                    <CircularProgress size={8} sx={{ animationDelay: '0.4s' }} />
                  </Box>
                </Paper>
              </Box>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </Box>
        
        {/* Input Area */}
        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <form onSubmit={handleInputSubmit}>
            <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
              <TextField
                ref={inputRef}
                fullWidth
                multiline
                maxRows={4}
                placeholder="Type your message..."
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                variant="outlined"
                size="small"
                disabled={!chatState.isConnected}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    bgcolor: 'background.paper',
                  },
                }}
                InputProps={{
                  endAdornment: (
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      <Tooltip title="Voice Message">
                        <IconButton
                          size="small"
                          onClick={handleVoiceRecording}
                          color={isRecording ? 'error' : 'default'}
                        >
                          <MicIcon />
                        </IconButton>
                      </Tooltip>
                      
                      <Tooltip title="Attach File">
                        <IconButton size="small">
                          <AttachFileIcon />
                        </IconButton>
                      </Tooltip>
                      
                      <Tooltip title="Emoji">
                        <IconButton size="small">
                          <EmojiIcon />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  ),
                }}
              />
              
              <Tooltip title="Send Message">
                <span>
                  <IconButton
                    type="submit"
                    color="primary"
                    disabled={!inputMessage.trim() || !chatState.isConnected}
                    sx={{
                      bgcolor: 'primary.main',
                      color: 'white',
                      '&:hover': { bgcolor: 'primary.dark' },
                      '&:disabled': { bgcolor: 'grey.300' },
                    }}
                  >
                    <SendIcon />
                  </IconButton>
                </span>
              </Tooltip>
            </Box>
          </form>
        </Box>
      </Paper>
      
      {/* Settings Drawer */}
      <Drawer
        anchor="right"
        open={chatState.showSettings}
        onClose={() => setChatState(prev => ({ ...prev, showSettings: false }))}
      >
        <Box sx={{ width: 300, p: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">Settings</Typography>
            <IconButton
              onClick={() => setChatState(prev => ({ ...prev, showSettings: false }))}
            >
              <CloseIcon />
            </IconButton>
          </Box>
          
          <Divider sx={{ mb: 2 }} />
          
          <List>
            <ListItem>
              <ListItemIcon>
                <TranslateIcon />
              </ListItemIcon>
              <ListItemText primary="Language" secondary="English" />
            </ListItem>
            
            <ListItem>
              <ListItemIcon>
                <FeedbackIcon />
              </ListItemIcon>
              <ListItemText primary="Send Feedback" />
            </ListItem>
          </List>
        </Box>
      </Drawer>
    </Box>
  );
};

export default ChatInterface; 