#!/bin/bash

# Installation script for PaisaTrack on Ubuntu (Oracle Cloud)
# This script installs all dependencies, configures nginx, and starts the application

# Terminal styling variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Icon variables
CHECKMARK='\xE2\x9C\x94'
CROSS='\xE2\x9D\x8C'
ARROW='\xE2\x96\xB6'
STAR='\xE2\xAD\x90'
WARNING='\xE2\x9A\xA0'

# Function to print styled messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[${CHECKMARK}] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[${WARNING}] $1${NC}"
}

print_error() {
    echo -e "${RED}[${CROSS}] $1${NC}"
}

# Function to simulate loading with percentage
show_loading() {
    local duration=$1
    local message=$2
    local interval=0.2
    local steps=$(echo "$duration / $interval" | bc -l | cut -d. -f1)
    
    echo -ne "${CYAN}[${ARROW}] ${message} [                    ]   0%${NC}\r"
    
    for i in $(seq 1 $steps); do
        local progress=$((i * 100 / steps))
        local bar_length=$((progress / 5))
        local bar=$(printf "%-${bar_length}s" "=" | tr ' ' '=')
        local spaces=$(printf "%-$((20 - bar_length))s" " ")
        
        echo -ne "${CYAN}[${ARROW}] ${message} [${bar}${spaces}] ${progress}%${NC}\r"
        sleep $interval
    done
    
    echo -e "${GREEN}[${CHECKMARK}] ${message} [====================] 100%${NC}"
}

# Function to test nginx with curl
test_nginx() {
    local server_ip=$1
    local port=$2
    
    print_status "Testing nginx configuration with curl..."
    
    # Wait a moment for services to start
    sleep 3
    
    # Test with curl
    response=$(curl -s -o /dev/null -w "%{http_code}" http://$server_ip:$port 2>/dev/null)
    
    if [ "$response" == "200" ]; then
        print_success "Nginx is successfully serving content on http://$server_ip:$port (HTTP $response)"
        return 0
    elif [ "$response" == "000" ]; then
        print_error "Failed to connect to http://$server_ip:$port - service may not be running"
        return 1
    else
        print_warning "Received HTTP $response from http://$server_ip:$port"
        return 1
    fi
}

# Main installation process
clear
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    PAISATRACK INSTALLATION SCRIPT                            ║"
echo "║                             for Ubuntu                                       ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

print_status "This script will install all required dependencies and configure the application."

# Update package list
print_status "Updating package list..."
show_loading 3 "Updating package list"
sudo apt update > /dev/null 2>&1

# Install required packages
print_status "Installing git, python3, pip, and nginx..."
show_loading 10 "Installing packages"
sudo apt install -y git python3 python3-pip nginx > /dev/null 2>&1

# Ask for repository URL
echo ""
echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ Please enter the repository URL to clone:                                   │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────────────────────────────┘${NC}"
read -p "Repository URL: " REPO_URL

# Clone repository
print_status "Cloning repository..."
show_loading 8 "Cloning repository"
git clone $REPO_URL > /dev/null 2>&1
REPO_NAME=$(basename "$REPO_URL" .git)
print_success "Repository cloned to ./$REPO_NAME"

# Install Python requirements
print_status "Installing Python requirements..."
show_loading 15 "Installing Python packages"
cd $REPO_NAME
pip3 install -r requirements.txt > /dev/null 2>&1

# Ask for environment variables
echo ""
echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ Environment Variables Setup                                                 │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────────────────────────────┘${NC}"
print_status "Please enter your MongoDB Atlas connection string:"
read -p "MongoDB Atlas URL: " MONGO_URL

# Create .env file
print_status "Creating environment configuration..."
show_loading 3 "Creating .env file"

cat > .env <<EOF
MONGO_URI=$MONGO_URL
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
EOF

print_success "Environment file created with MongoDB Atlas URL"

# Ask for additional environment variables
echo ""
print_status "Do you want to add any additional environment variables? (y/N):"
read ADD_ENV
if [[ $ADD_ENV =~ ^[Yy]$ ]]; then
    while true; do
        echo ""
        print_status "Enter variable name (or 'done' to finish):"
        read VAR_NAME
        if [[ $VAR_NAME == "done" ]]; then
            break
        fi
        print_status "Enter value for $VAR_NAME:"
        read VAR_VALUE
        echo "$VAR_NAME=$VAR_VALUE" >> .env
        print_success "Added $VAR_NAME to environment file"
    done
fi

# Initialize MongoDB (run init script to set up collections)
print_status "Initializing database collections..."
show_loading 8 "Setting up database"
python3 init_mongo.py > /dev/null 2>&1
print_success "Database collections initialized successfully"

# Ask for server IP and port
echo ""
echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ Please enter your server IP address:                                        │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────────────────────────────┘${NC}"
read -p "Server IP: " SERVER_IP

echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ Please enter the port (default is 5000):                                    │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────────────────────────────┘${NC}"
read -p "Port [5000]: " PORT
if [ -z "$PORT" ]; then
    PORT=5000
fi

# Create nginx configuration
print_status "Configuring nginx..."
show_loading 5 "Configuring nginx"

sudo tee /etc/nginx/sites-available/paisatrack > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_IP;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable the nginx site
sudo ln -sf /etc/nginx/sites-available/paisatrack /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
print_status "Testing nginx configuration..."
if sudo nginx -t > /dev/null 2>&1; then
    print_success "Nginx configuration test passed"
else
    print_error "Nginx configuration test failed"
    exit 1
fi

# Restart nginx
print_status "Restarting nginx..."
show_loading 5 "Restarting nginx"
sudo systemctl restart nginx > /dev/null 2>&1

# Create a systemd service file for the Python app
print_status "Creating systemd service for the Python application..."
show_loading 5 "Creating service file"

sudo tee /etc/systemd/system/paisatrack.service > /dev/null <<EOF
[Unit]
Description=PaisaTrack Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/ubuntu/$REPO_NAME
EnvironmentFile=/home/ubuntu/$REPO_NAME/.env
ExecStart=/usr/bin/python3 /home/ubuntu/$REPO_NAME/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start the service
print_status "Starting PaisaTrack service..."
show_loading 8 "Starting service"
sudo systemctl daemon-reload > /dev/null 2>&1
sudo systemctl enable paisatrack > /dev/null 2>&1
sudo systemctl start paisatrack > /dev/null 2>&1

# Test nginx with curl
test_nginx $SERVER_IP 80

# Display status
echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                          INSTALLATION COMPLETE                               ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
print_success "PaisaTrack has been installed and started."
echo -e "${GREEN}${STAR}${NC} Application is running on: http://$SERVER_IP"
echo ""
print_status "Environment variables have been configured in .env file"
print_status "To check the application status, you can use:"
echo "  sudo systemctl status paisatrack"
echo ""
print_status "To view application logs:"
echo "  sudo journalctl -u paisatrack -f"
echo ""
print_status "To restart the application:"
echo "  sudo systemctl restart paisatrack"
echo ""
print_status "New features include user authentication with JWT tokens."
echo "Users can now register, login, and have their own private financial data."
echo ""