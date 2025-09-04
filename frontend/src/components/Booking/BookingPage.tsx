import React from 'react';
import { Container, Typography, Box, Card, CardContent } from '@mui/material';

const BookingPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box textAlign="center" mb={4}>
        <Typography variant="h2" component="h1" className="gradient-text" gutterBottom>
          Book Your Course
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Schedule your educational journey with us
        </Typography>
      </Box>

      <Card className="hover-lift">
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Coming Soon
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Our booking system is currently under development. 
            Please contact our support team for course enrollment assistance.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default BookingPage; 