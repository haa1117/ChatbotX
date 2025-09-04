import React from 'react';
import {
  Box,
  Typography,
  Button,
  Grid,
  Container,
  Card,
  CardContent,
  Avatar,
  Paper,
  Chip,
} from '@mui/material';
import {
  Chat as ChatIcon,
  School as SchoolIcon,
  Analytics as AnalyticsIcon,
  Language as LanguageIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <ChatIcon fontSize="large" />,
      title: 'Advanced AI Chat',
      description: 'Powered by Rasa NLU with contextual understanding and natural conversations.',
    },
    {
      icon: <SchoolIcon fontSize="large" />,
      title: 'Education Focus',
      description: 'Specialized for course information, enrollment, and academic support.',
    },
    {
      icon: <AnalyticsIcon fontSize="large" />,
      title: 'Real-time Analytics',
      description: 'Comprehensive insights and performance metrics for continuous improvement.',
    },
    {
      icon: <LanguageIcon fontSize="large" />,
      title: 'Multi-language',
      description: 'Support for multiple languages with automatic detection.',
    },
    {
      icon: <SpeedIcon fontSize="large" />,
      title: 'Fast & Reliable',
      description: 'Sub-200ms response times with 99.9% uptime guarantee.',
    },
    {
      icon: <SecurityIcon fontSize="large" />,
      title: 'Enterprise Security',
      description: 'SOC 2 Type II compliant with end-to-end encryption.',
    },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <Box textAlign="center" sx={{ mb: 8 }}>
            <Typography
              variant="h1"
              component="h1"
              sx={{
                fontSize: { xs: '2.5rem', md: '4rem' },
                fontWeight: 700,
                mb: 3,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                color: 'transparent',
              }}
            >
              ChatBotX
            </Typography>
            
            <Typography
              variant="h4"
              component="h2"
              sx={{ mb: 3, color: 'white', fontWeight: 300 }}
            >
              AI Support Assistant for Education
            </Typography>
            
            <Typography
              variant="h6"
              sx={{ mb: 4, color: 'rgba(255,255,255,0.8)', maxWidth: 600, mx: 'auto' }}
            >
              Revolutionize your educational support with our advanced AI chatbot. 
              Handle course inquiries, manage enrollments, and provide 24/7 student assistance.
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/chat')}
                sx={{
                  bgcolor: 'white',
                  color: 'primary.main',
                  px: 4,
                  py: 1.5,
                  fontSize: '1.1rem',
                  '&:hover': {
                    bgcolor: 'grey.100',
                  },
                }}
              >
                Try ChatBotX Now
              </Button>
              
              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate('/courses')}
                sx={{
                  borderColor: 'white',
                  color: 'white',
                  px: 4,
                  py: 1.5,
                  fontSize: '1.1rem',
                  '&:hover': {
                    borderColor: 'white',
                    bgcolor: 'rgba(255,255,255,0.1)',
                  },
                }}
              >
                Browse Courses
              </Button>
            </Box>
          </Box>
        </motion.div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <Paper
            elevation={8}
            sx={{
              p: 4,
              borderRadius: 4,
              background: 'rgba(255,255,255,0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255,255,255,0.2)',
            }}
          >
            <Grid container spacing={4} textAlign="center">
              <Grid item xs={12} md={3}>
                <Typography variant="h3" sx={{ color: 'white', fontWeight: 700 }}>
                  40%
                </Typography>
                <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                  Reduction in Support Workload
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <Typography variant="h3" sx={{ color: 'white', fontWeight: 700 }}>
                  95%+
                </Typography>
                <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                  Intent Recognition Accuracy
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <Typography variant="h3" sx={{ color: 'white', fontWeight: 700 }}>
                  24/7
                </Typography>
                <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                  Available Support
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <Typography variant="h3" sx={{ color: 'white', fontWeight: 700 }}>
                  &lt;200ms
                </Typography>
                <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                  Average Response Time
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </motion.div>
      </Container>

      {/* Features Section */}
      <Box sx={{ bgcolor: 'background.default', py: 8 }}>
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Typography
              variant="h2"
              component="h3"
              textAlign="center"
              sx={{ mb: 6, color: 'text.primary' }}
            >
              Powerful Features
            </Typography>
            
            <Grid container spacing={4}>
              {features.map((feature, index) => (
                <Grid item xs={12} md={6} lg={4} key={index}>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.1 * index }}
                  >
                    <Card
                      elevation={2}
                      sx={{
                        height: '100%',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          transform: 'translateY(-8px)',
                          boxShadow: 8,
                        },
                      }}
                    >
                      <CardContent sx={{ p: 4, textAlign: 'center' }}>
                        <Avatar
                          sx={{
                            bgcolor: 'primary.main',
                            width: 64,
                            height: 64,
                            mx: 'auto',
                            mb: 3,
                          }}
                        >
                          {feature.icon}
                        </Avatar>
                        
                        <Typography variant="h5" component="h4" sx={{ mb: 2 }}>
                          {feature.title}
                        </Typography>
                        
                        <Typography variant="body1" color="text.secondary">
                          {feature.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </motion.div>
        </Container>
      </Box>

      {/* Technologies Section */}
      <Box sx={{ py: 8 }}>
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            <Typography
              variant="h2"
              component="h3"
              textAlign="center"
              sx={{ mb: 6, color: 'white' }}
            >
              Built with Modern Technologies
            </Typography>
            
            <Box sx={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: 2 }}>
              {['React', 'TypeScript', 'Rasa', 'FastAPI', 'MongoDB', 'Redis', 'Material-UI', 'Docker'].map((tech) => (
                <Chip
                  key={tech}
                  label={tech}
                  variant="outlined"
                  sx={{
                    color: 'white',
                    borderColor: 'white',
                    fontSize: '1rem',
                    py: 2,
                    px: 3,
                    '&:hover': {
                      bgcolor: 'rgba(255,255,255,0.1)',
                    },
                  }}
                />
              ))}
            </Box>
          </motion.div>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box sx={{ bgcolor: 'background.default', py: 8 }}>
        <Container maxWidth="md">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <Paper
              elevation={8}
              sx={{
                p: 6,
                textAlign: 'center',
                borderRadius: 4,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
              }}
            >
              <Typography variant="h3" component="h3" sx={{ mb: 3 }}>
                Ready to Transform Your Education Support?
              </Typography>
              
              <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
                Join thousands of educational institutions already using ChatBotX
              </Typography>
              
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/chat')}
                sx={{
                  bgcolor: 'white',
                  color: 'primary.main',
                  px: 6,
                  py: 2,
                  fontSize: '1.2rem',
                  '&:hover': {
                    bgcolor: 'grey.100',
                  },
                }}
              >
                Start Your Free Trial
              </Button>
            </Paper>
          </motion.div>
        </Container>
      </Box>
    </Box>
  );
};

export default LandingPage; 