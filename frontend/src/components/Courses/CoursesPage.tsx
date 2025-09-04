import React from 'react';
import { Container, Typography, Box, Card, CardContent } from '@mui/material';

const CoursesPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box textAlign="center" mb={4}>
        <Typography variant="h2" component="h1" className="gradient-text" gutterBottom>
          Our Courses
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Explore our educational programs
        </Typography>
      </Box>

      <Card className="hover-lift">
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Course Catalog
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Our comprehensive course catalog is being prepared. 
            Soon you'll be able to browse and enroll in various educational programs 
            including programming, data science, AI, and more.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default CoursesPage; 