#!/bin/bash
# Cursor Stats Dashboard - macOS/Linux Setup Script
# This script creates a virtual environment and installs all dependencies safely

echo ""
echo "========================================"
echo "  Cursor Stats Dashboard - Setup"
echo "  macOS/Linux Installation"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Step 1: Check Python
echo -e "${YELLOW}[1/7] Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}  ✓ Found: $PYTHON_VERSION${NC}"
    
    # Check version
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        echo -e "${RED}  ✗ Python 3.8+ required (found $PYTHON_VERSION)${NC}"
        echo -e "${YELLOW}  Download from: https://www.python.org/downloads/${NC}"
        exit 1
    fi
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1)
    echo -e "${GREEN}  ✓ Found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}  ✗ Python not found${NC}"
    echo -e "${YELLOW}  Download from: https://www.python.org/downloads/${NC}"
    exit 1
fi

# Step 2: Check Node.js
echo ""
echo -e "${YELLOW}[2/7] Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version 2>&1)
    echo -e "${GREEN}  ✓ Found Node.js: $NODE_VERSION${NC}"
    
    # Check version
    NODE_MAJOR=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_MAJOR" -lt 16 ]; then
        echo -e "${RED}  ✗ Node.js 16+ required (found $NODE_VERSION)${NC}"
        echo -e "${YELLOW}  Download from: https://nodejs.org/${NC}"
        exit 1
    fi
    
    NPM_VERSION=$(npm --version 2>&1)
    echo -e "${GREEN}  ✓ Found npm: v$NPM_VERSION${NC}"
else
    echo -e "${RED}  ✗ Node.js not found${NC}"
    echo -e "${YELLOW}  Download from: https://nodejs.org/${NC}"
    exit 1
fi

# Step 3: Create virtual environment
echo ""
echo -e "${YELLOW}[3/7] Creating isolated Python environment...${NC}"
echo -e "  ${NC}(This keeps packages separate from your system Python)${NC}"
cd "$ROOT_DIR"

if [ -d "venv" ]; then
    echo -e "${GREEN}  ✓ Virtual environment already exists${NC}"
else
    if $PYTHON_CMD -m venv venv; then
        echo -e "${GREEN}  ✓ Virtual environment created${NC}"
    else
        echo -e "${RED}  ✗ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Step 4: Install Python dependencies (root)
echo ""
echo -e "${YELLOW}[4/7] Installing Python packages (stats engine)...${NC}"
if pip install -r requirements.txt > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Python packages installed${NC}"
else
    echo -e "${RED}  ✗ Failed to install Python packages${NC}"
    echo -e "${YELLOW}  Try running manually after activating venv${NC}"
    exit 1
fi

# Step 5: Install backend dependencies
echo ""
echo -e "${YELLOW}[5/7] Installing backend packages (FastAPI)...${NC}"
if pip install -r backend/requirements.txt > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Backend packages installed${NC}"
else
    echo -e "${RED}  ✗ Failed to install backend packages${NC}"
    exit 1
fi

# Step 6: Install frontend dependencies
echo ""
echo -e "${YELLOW}[6/7] Installing frontend packages (React)...${NC}"
echo -e "  ${NC}This may take a few minutes...${NC}"
cd "$ROOT_DIR/frontend"
if npm install > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Frontend packages installed${NC}"
else
    echo -e "${RED}  ✗ Failed to install frontend packages${NC}"
    echo -e "${YELLOW}  Try running manually: cd frontend && npm install${NC}"
    exit 1
fi

# Step 7: Verify installation
echo ""
echo -e "${YELLOW}[7/7] Verifying installation...${NC}"
cd "$ROOT_DIR"
ALL_GOOD=true

# Check Python packages
if python -c "import numpy, fastapi, uvicorn" 2> /dev/null; then
    echo -e "${GREEN}  ✓ Python packages verified${NC}"
else
    echo -e "${RED}  ✗ Python packages not working${NC}"
    ALL_GOOD=false
fi

# Check frontend packages
if [ -d "$ROOT_DIR/frontend/node_modules/react" ]; then
    echo -e "${GREEN}  ✓ Frontend packages verified${NC}"
else
    echo -e "${RED}  ✗ Frontend packages not found${NC}"
    ALL_GOOD=false
fi

# Deactivate venv
deactivate

# Create launch script in setup folder
cat > "$SCRIPT_DIR/launch.sh" << 'EOF'
#!/bin/bash
# Activate virtual environment and launch dashboard
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"
source venv/bin/activate
python launch_dashboard.py
EOF
chmod +x "$SCRIPT_DIR/launch.sh"

# Final message
echo ""
echo "========================================"
if [ "$ALL_GOOD" = true ]; then
    echo -e "${GREEN}  Setup Complete! 🎉${NC}"
    echo "========================================"
    echo ""
    echo -e "${CYAN}✓ Virtual environment created (safe & isolated)${NC}"
    echo -e "${CYAN}✓ All packages installed${NC}"
    echo -e "${CYAN}✓ Ready to use!${NC}"
    echo ""
    echo -e "${YELLOW}To launch the dashboard:${NC}"
    echo -e "  ${CYAN}cd setup${NC}"
    echo -e "  ${CYAN}./launch.sh${NC}"
    echo ""
    echo -e "  ${NC}Or manually:${NC}"
    echo -e "  ${CYAN}cd ..${NC}"
    echo -e "  ${CYAN}source venv/bin/activate${NC}"
    echo -e "  ${CYAN}python launch_dashboard.py${NC}"
    echo ""
    echo -e "${NC}The dashboard will open at http://localhost:5173${NC}"
else
    echo -e "${YELLOW}  Setup Had Issues ⚠️${NC}"
    echo "========================================"
    echo ""
    echo -e "${YELLOW}Some packages may not be installed correctly.${NC}"
    echo -e "${YELLOW}See INSTALLATION.md for manual setup steps${NC}"
fi
echo ""
