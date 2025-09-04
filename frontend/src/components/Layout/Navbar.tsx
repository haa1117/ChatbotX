import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  IconButton,
} from '@mui/material';
import { Chat as ChatIcon, Menu as MenuIcon } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <AppBar position="static" elevation={0} sx={{ background: 'transparent' }}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <Avatar sx={{ bgcolor: 'secondary.main', mr: 2 }}>
            <ChatIcon />
          </Avatar>
          <Typography
            variant="h6"
            component="div"
            sx={{ color: 'white', fontWeight: 600 }}
          >
            ChatBotX
          </Typography>
        </Box>

        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
          <Button
            color="inherit"
            onClick={() => navigate('/')}
            sx={{
              color: 'white',
              fontWeight: isActive('/') ? 600 : 400,
              textDecoration: isActive('/') ? 'underline' : 'none',
            }}
          >
            Home
          </Button>
          <Button
            color="inherit"
            onClick={() => navigate('/chat')}
            sx={{
              color: 'white',
              fontWeight: isActive('/chat') ? 600 : 400,
              textDecoration: isActive('/chat') ? 'underline' : 'none',
            }}
          >
            Chat
          </Button>
          <Button
            color="inherit"
            onClick={() => navigate('/courses')}
            sx={{
              color: 'white',
              fontWeight: isActive('/courses') ? 600 : 400,
              textDecoration: isActive('/courses') ? 'underline' : 'none',
            }}
          >
            Courses
          </Button>
          <Button
            color="inherit"
            onClick={() => navigate('/faq')}
            sx={{
              color: 'white',
              fontWeight: isActive('/faq') ? 600 : 400,
              textDecoration: isActive('/faq') ? 'underline' : 'none',
            }}
          >
            FAQ
          </Button>
        </Box>

        <IconButton
          color="inherit"
          sx={{ display: { xs: 'flex', md: 'none' }, color: 'white' }}
        >
          <MenuIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 