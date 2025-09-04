import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Course {
  id: string;
  course_code: string;
  title: string;
  description: string;
  category: string;
  duration: string;
  price: number;
  currency: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  status: 'active' | 'inactive' | 'draft';
  max_students: number;
  enrolled_students: number;
  instructor: string;
  start_date: string;
  end_date: string;
  schedule: string;
  created_at: string;
  updated_at: string;
}

interface CoursesState {
  courses: Course[];
  filteredCourses: Course[];
  selectedCourse: Course | null;
  categories: string[];
  isLoading: boolean;
  error: string | null;
  filters: {
    category: string;
    level: string;
    priceRange: [number, number];
    searchQuery: string;
  };
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}

const initialState: CoursesState = {
  courses: [],
  filteredCourses: [],
  selectedCourse: null,
  categories: [],
  isLoading: false,
  error: null,
  filters: {
    category: '',
    level: '',
    priceRange: [0, 1000],
    searchQuery: '',
  },
  pagination: {
    page: 1,
    limit: 12,
    total: 0,
  },
};

export const coursesSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {
    setCourses: (state, action: PayloadAction<Course[]>) => {
      state.courses = action.payload;
      state.filteredCourses = action.payload;
      state.isLoading = false;
      state.error = null;
    },
    setSelectedCourse: (state, action: PayloadAction<Course>) => {
      state.selectedCourse = action.payload;
    },
    setCategories: (state, action: PayloadAction<string[]>) => {
      state.categories = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
    setFilters: (state, action: PayloadAction<Partial<CoursesState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    setPagination: (state, action: PayloadAction<Partial<CoursesState['pagination']>>) => {
      state.pagination = { ...state.pagination, ...action.payload };
    },
    filterCourses: (state) => {
      let filtered = [...state.courses];
      
      // Filter by category
      if (state.filters.category) {
        filtered = filtered.filter(course => course.category === state.filters.category);
      }
      
      // Filter by level
      if (state.filters.level) {
        filtered = filtered.filter(course => course.level === state.filters.level);
      }
      
      // Filter by price range
      filtered = filtered.filter(course => 
        course.price >= state.filters.priceRange[0] && 
        course.price <= state.filters.priceRange[1]
      );
      
      // Filter by search query
      if (state.filters.searchQuery) {
        const query = state.filters.searchQuery.toLowerCase();
        filtered = filtered.filter(course =>
          course.title.toLowerCase().includes(query) ||
          course.description.toLowerCase().includes(query) ||
          course.instructor.toLowerCase().includes(query)
        );
      }
      
      state.filteredCourses = filtered;
      state.pagination.total = filtered.length;
    },
    clearFilters: (state) => {
      state.filters = {
        category: '',
        level: '',
        priceRange: [0, 1000],
        searchQuery: '',
      };
      state.filteredCourses = state.courses;
    },
  },
});

export const {
  setCourses,
  setSelectedCourse,
  setCategories,
  setLoading,
  setError,
  setFilters,
  setPagination,
  filterCourses,
  clearFilters,
} = coursesSlice.actions;

export default coursesSlice.reducer; 