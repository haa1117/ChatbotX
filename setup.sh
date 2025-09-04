#!/bin/bash

# ChatBotX - AI Support Assistant Setup Script
# This script sets up the complete ChatBotX environment

set -e

echo "🚀 ChatBotX - AI Support Assistant Setup"
echo "========================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if running on supported OS
check_os() {
    print_header "🔍 Checking Operating System..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_status "Linux detected"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_status "macOS detected"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="windows"
        print_status "Windows detected"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    print_header "🔧 Checking Prerequisites..."
    
    # Check for Node.js
    if command -v node >/dev/null 2>&1; then
        NODE_VERSION=$(node --version)
        print_status "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/"
        exit 1
    fi
    
    # Check for Python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version)
        print_status "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3.9+ is not installed. Please install Python from https://python.org/"
        exit 1
    fi
    
    # Check for Docker
    if command -v docker >/dev/null 2>&1; then
        DOCKER_VERSION=$(docker --version)
        print_status "Docker found: $DOCKER_VERSION"
    else
        print_warning "Docker not found. Docker is optional but recommended for full deployment."
    fi
    
    # Check for MongoDB
    if command -v mongod >/dev/null 2>&1; then
        MONGO_VERSION=$(mongod --version | head -n 1)
        print_status "MongoDB found: $MONGO_VERSION"
    else
        print_warning "MongoDB not found. Please install MongoDB or use Docker."
    fi
    
    # Check for Redis
    if command -v redis-server >/dev/null 2>&1; then
        REDIS_VERSION=$(redis-server --version)
        print_status "Redis found: $REDIS_VERSION"
    else
        print_warning "Redis not found. Please install Redis or use Docker."
    fi
}

# Setup environment files
setup_environment() {
    print_header "📝 Setting up Environment Files..."
    
    # Backend environment
    if [ ! -f "backend/.env" ]; then
        print_status "Creating backend .env file..."
        cat > backend/.env << EOF
# ChatBotX Backend Configuration
DEBUG=True
SECRET_KEY=chatbotx-dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=chatbotx

# Redis
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# Rasa
RASA_SERVER_URL=http://localhost:5005

# Features
ENABLE_ANALYTICS=True
ENABLE_SENTIMENT_ANALYSIS=True
ENABLE_LANGUAGE_DETECTION=True
SUPPORTED_LANGUAGES=en,es,fr,de
DEFAULT_LANGUAGE=en

# File Upload
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=.pdf,.doc,.docx,.txt,.png,.jpg,.jpeg

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Logging
LOG_LEVEL=INFO
EOF
        print_status "Backend .env file created"
    else
        print_status "Backend .env file already exists"
    fi
    
    # Frontend environment
    if [ ! -f "frontend/.env" ]; then
        print_status "Creating frontend .env file..."
        cat > frontend/.env << EOF
# ChatBotX Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_APP_NAME=ChatBotX
REACT_APP_VERSION=1.0.0
EOF
        print_status "Frontend .env file created"
    else
        print_status "Frontend .env file already exists"
    fi
}

# Install backend dependencies
install_backend() {
    print_header "🐍 Installing Backend Dependencies..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate || source venv/Scripts/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python packages..."
    pip install -r requirements.txt
    
    print_status "Backend dependencies installed successfully!"
    cd ..
}

# Install frontend dependencies
install_frontend() {
    print_header "⚛️ Installing Frontend Dependencies..."
    
    cd frontend
    
    # Install npm dependencies
    print_status "Installing npm packages..."
    npm install
    
    print_status "Frontend dependencies installed successfully!"
    cd ..
}

# Setup Rasa
setup_rasa() {
    print_header "🤖 Setting up Rasa..."
    
    cd rasa
    
    # Install Rasa if not already installed
    if ! command -v rasa >/dev/null 2>&1; then
        print_status "Installing Rasa..."
        pip install rasa
    fi
    
    # Download spaCy model
    print_status "Downloading spaCy English model..."
    python -m spacy download en_core_web_md
    
    # Train initial model
    print_status "Training initial Rasa model..."
    rasa train
    
    print_status "Rasa setup completed!"
    cd ..
}

# Setup databases
setup_databases() {
    print_header "🗄️ Setting up Databases..."
    
    # MongoDB setup
    if command -v mongod >/dev/null 2>&1; then
        print_status "Starting MongoDB..."
        if [[ "$OS" == "linux" ]]; then
            sudo systemctl start mongod || sudo service mongod start
        elif [[ "$OS" == "macos" ]]; then
            brew services start mongodb-community || mongod --config /usr/local/etc/mongod.conf --fork
        fi
        print_status "MongoDB started"
    else
        print_warning "MongoDB not found. Please start MongoDB manually or use Docker."
    fi
    
    # Redis setup
    if command -v redis-server >/dev/null 2>&1; then
        print_status "Starting Redis..."
        if [[ "$OS" == "linux" ]]; then
            sudo systemctl start redis || sudo service redis start
        elif [[ "$OS" == "macos" ]]; then
            brew services start redis || redis-server --daemonize yes
        fi
        print_status "Redis started"
    else
        print_warning "Redis not found. Please start Redis manually or use Docker."
    fi
}

# Create necessary directories
create_directories() {
    print_header "📁 Creating Directories..."
    
    mkdir -p backend/uploads
    mkdir -p backend/logs
    mkdir -p backend/static
    mkdir -p rasa/models
    mkdir -p rasa/data
    
    print_status "Directories created successfully!"
}

# Docker setup (optional)
setup_docker() {
    print_header "🐳 Docker Setup (Optional)..."
    
    if command -v docker >/dev/null 2>&1; then
        read -p "Would you like to use Docker for deployment? (y/n): " use_docker
        
        if [[ $use_docker == "y" || $use_docker == "Y" ]]; then
            print_status "Building Docker containers..."
            docker-compose build
            
            print_status "Starting services with Docker..."
            docker-compose up -d mongodb redis
            
            print_status "Docker setup completed!"
        fi
    else
        print_warning "Docker not available. Skipping Docker setup."
    fi
}

# Test installation
test_installation() {
    print_header "🧪 Testing Installation..."
    
    # Test backend
    print_status "Testing backend..."
    cd backend
    source venv/bin/activate || source venv/Scripts/activate
    
    # Start backend in background for testing
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Wait a moment for startup
    sleep 5
    
    # Test health endpoint
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        print_status "Backend health check passed!"
    else
        print_warning "Backend health check failed. Please check the logs."
    fi
    
    # Stop backend
    kill $BACKEND_PID 2>/dev/null || true
    
    cd ..
    
    # Test frontend build
    print_status "Testing frontend build..."
    cd frontend
    npm run build >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_status "Frontend build successful!"
    else
        print_warning "Frontend build failed. Please check for errors."
    fi
    cd ..
}

# Show final instructions
show_instructions() {
    print_header "🎉 Setup Complete!"
    echo ""
    echo "ChatBotX has been set up successfully! Here's how to run it:"
    echo ""
    echo "🚀 Quick Start:"
    echo "1. Start the backend:"
    echo "   cd backend"
    echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo "   python -m uvicorn app.main:app --reload --port 8000"
    echo ""
    echo "2. Start Rasa (in another terminal):"
    echo "   cd rasa"
    echo "   rasa run --enable-api --cors \"*\" --port 5005"
    echo ""
    echo "3. Start the frontend (in another terminal):"
    echo "   cd frontend"
    echo "   npm start"
    echo ""
    echo "🌐 Access the application:"
    echo "- Frontend: http://localhost:3000"
    echo "- Backend API: http://localhost:8000"
    echo "- API Documentation: http://localhost:8000/docs"
    echo "- Rasa API: http://localhost:5005"
    echo ""
    echo "🐳 Docker Alternative:"
    echo "   docker-compose up"
    echo ""
    echo "📚 Documentation:"
    echo "- Check README.md for detailed information"
    echo "- API docs available at /docs endpoint"
    echo "- Configuration files are in backend/.env and frontend/.env"
    echo ""
    echo "🆘 Need Help?"
    echo "- Check the logs in backend/logs/"
    echo "- Ensure MongoDB and Redis are running"
    echo "- Review environment variables in .env files"
    echo ""
    print_status "Happy coding with ChatBotX! 🤖✨"
}

# Main setup flow
main() {
    check_os
    check_prerequisites
    create_directories
    setup_environment
    install_backend
    install_frontend
    setup_rasa
    setup_databases
    setup_docker
    test_installation
    show_instructions
}

# Run main function
main 