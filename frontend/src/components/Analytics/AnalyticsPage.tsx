import React from 'react';
import { Container, Typography, Box, Card, CardContent } from '@mui/material';

const AnalyticsPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box textAlign="center" mb={4}>
        <Typography variant="h2" component="h1" className="gradient-text" gutterBottom>
          Analytics Dashboard
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Insights and Performance Metrics
        </Typography>
      </Box>

      <Card className="hover-lift">
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Analytics Coming Soon
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Comprehensive analytics and reporting features are being developed. 
            This will include chat performance metrics, user engagement statistics, and more.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default AnalyticsPage; 