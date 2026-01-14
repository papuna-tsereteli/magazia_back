#!/bin/bash

# MySQL Database Setup Script
# This script sets up the local MySQL database for the application

set -e

echo "=========================================="
echo "MySQL Database Setup"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Database configuration
DB_NAME="allsy"
DB_USER="allsy_user"
DB_PASSWORD="Marganeci123!"

echo -e "${GREEN}Step 1: Installing MySQL Server...${NC}"
sudo apt update
sudo apt install -y mysql-server

echo -e "${GREEN}Step 2: Starting MySQL service...${NC}"
sudo systemctl start mysql
sudo systemctl enable mysql

echo -e "${GREEN}Step 3: Creating database and user...${NC}"
sudo mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"
sudo mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo -e "${GREEN}Step 4: Verifying database connection...${NC}"
mysql -u${DB_USER} -p${DB_PASSWORD} -e "USE ${DB_NAME}; SELECT 'Database connection successful!' as Status;"

echo ""
echo -e "${GREEN}=========================================="
echo "MySQL setup completed successfully!"
echo "==========================================${NC}"
echo ""
echo "Database Details:"
echo "  Database: ${DB_NAME}"
echo "  User: ${DB_USER}"
echo "  Host: localhost"
echo "  Port: 3306"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Run Django migrations: python manage.py migrate"
echo "2. Create superuser: python manage.py createsuperuser"
