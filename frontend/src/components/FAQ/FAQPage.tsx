import React from 'react';
import { Container, Typography, Box, Card, CardContent } from '@mui/material';

const FAQPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box textAlign="center" mb={4}>
        <Typography variant="h2" component="h1" className="gradient-text" gutterBottom>
          Frequently Asked Questions
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Get answers to common questions
        </Typography>
      </Box>

      <Card className="hover-lift">
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            FAQ Section
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Our comprehensive FAQ section is being developed. 
            In the meantime, feel free to use our AI chatbot for immediate assistance 
            with your questions about courses, enrollment, and platform features.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default FAQPage; 