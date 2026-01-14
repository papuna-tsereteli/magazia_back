#!/bin/bash

# EC2 Deployment Script for VueShop Django Backend
# Run this script on your EC2 instance after uploading the project files

set -e  # Exit on error

echo "=========================================="
echo "VueShop Backend Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as ubuntu user
if [ "$USER" != "ubuntu" ]; then
    echo -e "${YELLOW}Warning: This script should be run as 'ubuntu' user${NC}"
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${GREEN}Step 1: Installing system packages...${NC}"
sudo apt update
sudo apt install -y python3-pip python3-dev python3-venv \
    libmysqlclient-dev build-essential \
    nginx git curl mysql-server

echo -e "${GREEN}Step 2: Setting up MySQL database...${NC}"
sudo systemctl start mysql
sudo systemctl enable mysql

# Check if .env.production exists, otherwise use .env
if [ -f .env.production ]; then
    echo "Using .env.production for database configuration..."
    cp .env.production .env
fi

# Read database configuration from .env file
DB_NAME=$(grep DB_NAME .env | cut -d '=' -f2)
DB_USER=$(grep DB_USER .env | cut -d '=' -f2)
DB_PASSWORD=$(grep DB_PASSWORD .env | cut -d '=' -f2)

echo "Database: ${DB_NAME}, User: ${DB_USER}"
echo "Creating database and user..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" || true
sudo mysql -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';" || true
sudo mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';" || true
sudo mysql -e "FLUSH PRIVILEGES;" || true

echo "Testing database connection..."
mysql -u${DB_USER} -p${DB_PASSWORD} -e "USE ${DB_NAME}; SELECT 'Connected!' as Status;" && echo -e "${GREEN}Database connection successful!${NC}"

echo -e "${GREEN}Step 3: Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${GREEN}Step 4: Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}Step 5: Checking environment variables...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please create .env file with database credentials"
    exit 1
fi

echo -e "${GREEN}Step 6: Running Django migrations...${NC}"
python manage.py migrate

echo -e "${GREEN}Step 7: Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}Step 8: Running Django deployment check...${NC}"
python manage.py check --deploy

echo -e "${GREEN}Step 9: Setting up Gunicorn service...${NC}"
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

echo -e "${GREEN}Step 10: Configuring Nginx...${NC}"
sudo cp nginx.conf /etc/nginx/sites-available/vueshop_backend
sudo ln -sf /etc/nginx/sites-available/vueshop_backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

echo -e "${GREEN}Step 11: Setting file permissions...${NC}"
sudo chown -R ubuntu:www-data "$SCRIPT_DIR"
sudo chmod -R 755 "$SCRIPT_DIR"
sudo chmod -R 775 "$SCRIPT_DIR/media"

echo -e "${GREEN}Step 12: Configuring firewall...${NC}"
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
echo "y" | sudo ufw enable

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment completed successfully!"
echo "==========================================${NC}"
echo ""
echo "Service Status:"
sudo systemctl status gunicorn --no-pager -l
echo ""
sudo systemctl status nginx --no-pager -l
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create Django superuser: python manage.py createsuperuser"
echo "2. Configure SSL: sudo certbot --nginx -d api.allsy.ge"
echo "3. Test the API: curl http://localhost:8000"
echo ""
echo "View logs:"
echo "  Gunicorn: sudo journalctl -u gunicorn -f"
echo "  Nginx: sudo tail -f /var/log/nginx/error.log"
