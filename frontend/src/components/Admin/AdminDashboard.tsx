import React from 'react';
import { Container, Typography, Box, Card, CardContent } from '@mui/material';

const AdminDashboard: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box textAlign="center" mb={4}>
        <Typography variant="h2" component="h1" className="gradient-text" gutterBottom>
          Admin Dashboard
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Manage your ChatBotX system
        </Typography>
      </Box>

      <Card className="hover-lift">
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Admin Panel
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Administrator features are currently being developed. 
            This will include user management, analytics, and system configuration.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default AdminDashboard; 