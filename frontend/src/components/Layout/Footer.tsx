import React from 'react';
import { Box, Container, Typography, Link, Grid } from '@mui/material';

const Footer: React.FC = () => {
  return (
    <Box
      component="footer"
      sx={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        py: 4,
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              ChatBotX
            </Typography>
            <Typography variant="body2">
              AI-powered support assistant for educational institutions.
              Enhancing student experience through intelligent automation.
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              Quick Links
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Link href="/" color="inherit" underline="hover">
                Home
              </Link>
              <Link href="/courses" color="inherit" underline="hover">
                Courses
              </Link>
              <Link href="/chat" color="inherit" underline="hover">
                Chat Support
              </Link>
              <Link href="/faq" color="inherit" underline="hover">
                FAQ
              </Link>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              Contact
            </Typography>
            <Typography variant="body2">
              Email: support@chatbotx.com
            </Typography>
            <Typography variant="body2">
              Phone: (555) 123-4567
            </Typography>
            <Typography variant="body2">
              Available 24/7 via AI Chat
            </Typography>
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 4, pt: 2, borderTop: '1px solid rgba(255,255,255,0.2)' }}>
          <Typography variant="body2" align="center">
            © 2024 ChatBotX. All rights reserved. | Built with ❤️ for Education
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer; 