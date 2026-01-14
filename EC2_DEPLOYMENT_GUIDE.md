# EC2 Production Deployment Guide

This guide will help you deploy the VueShop Django Backend to AWS EC2.

## Prerequisites

- AWS EC2 instance running Ubuntu 20.04 or later
- EC2 instance with public IP: 63.176.47.213
- Domain: api.allsy.ge pointing to EC2 IP
- SSH access to EC2 instance
- Local MySQL database will be installed on EC2

## Step 1: Initial Server Setup

```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@63.176.47.213

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages (including MySQL)
sudo apt install -y python3-pip python3-dev python3-venv \
    libmysqlclient-dev build-essential \
    nginx git curl mysql-server
```

## Step 2: Set Up MySQL Database

```bash
# Start and enable MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Create database and user
sudo mysql -e "CREATE DATABASE IF NOT EXISTS allsy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'allsy_user'@'localhost' IDENTIFIED BY 'Marganeci123!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON allsy.* TO 'allsy_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Test connection
mysql -uallsy_user -pMarganeci123! -e "USE allsy; SELECT 'Connected!' as Status;"
```

**Note**: You can also use the provided `setup_mysql.sh` script:
```bash
chmod +x setup_mysql.sh
./setup_mysql.sh
```

## Step 3: Set Up Application Directory

```bash
# Navigate to home directory
cd /home/ubuntu

# Clone your repository (or upload files via SCP/SFTP)
# Option 1: Clone from Git
git clone <your-repo-url> magazia_back
# Option 2: Upload files directly
# scp -i your-key.pem -r C:\Users\paguna\Desktop\magazia_back ubuntu@63.176.47.213:/home/ubuntu/

cd magazia_back
```

## Step 4: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

```bash
# Create .env file (if not uploaded)
nano .env

# Add the following (adjust values as needed):
```

```env
# MySQL Local Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=allsy
DB_USER=allsy_user
DB_PASSWORD=Marganeci123!
DB_HOST=localhost
DB_PORT=3306

# Django Secret Key (generate a new one for production!)
SECRET_KEY=w4frfloa^!_w9n%62c2z_uq10*03s*05+-gfp&t67o#vhmy9zx
```

**IMPORTANT**: Generate a new SECRET_KEY for production:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Step 6: Configure Django

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test that everything works
python manage.py check --deploy
```

## Step 7: Set Up Gunicorn Service

```bash
# Copy the systemd service file
sudo cp gunicorn.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable Gunicorn to start on boot
sudo systemctl enable gunicorn

# Start Gunicorn
sudo systemctl start gunicorn

# Check status
sudo systemctl status gunicorn

# View logs if needed
sudo journalctl -u gunicorn -f
```

## Step 8: Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/vueshop_backend

# Create symbolic link to enable site
sudo ln -s /etc/nginx/sites-available/vueshop_backend /etc/nginx/sites-enabled/

# Remove default nginx site
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Enable nginx to start on boot
sudo systemctl enable nginx
```

## Step 9: Configure Firewall

```bash
# Allow SSH (port 22)
sudo ufw allow 22

# Allow HTTP (port 80)
sudo ufw allow 80

# Allow HTTPS (port 443)
sudo ufw allow 443

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## Step 10: Configure File Permissions

```bash
# Set proper ownership
sudo chown -R ubuntu:www-data /home/ubuntu/magazia_back

# Set proper permissions
sudo chmod -R 755 /home/ubuntu/magazia_back

# Media directory needs write permissions
sudo chmod -R 775 /home/ubuntu/magazia_back/media
```

## Step 11: Test the Deployment

```bash
# Check if Gunicorn is running
sudo systemctl status gunicorn

# Check if Nginx is running
sudo systemctl status nginx

# Test the API
curl http://localhost:8000
curl http://63.176.47.213
```

## Step 12: SSL/HTTPS Setup (Recommended)

```bash
# Install Certbot for Let's Encrypt SSL
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d api.allsy.ge

# Certbot will automatically configure nginx for HTTPS
# Follow the prompts to complete SSL setup

# Test auto-renewal
sudo certbot renew --dry-run
```

After SSL is configured, update settings.py if needed:
- SECURE_SSL_REDIRECT is already set to True in production
- Make sure your domain properly points to the EC2 IP

## Common Management Commands

### Restart Gunicorn
```bash
sudo systemctl restart gunicorn
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

### View Gunicorn Logs
```bash
sudo journalctl -u gunicorn -f
```

### View Nginx Logs
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Update Application Code
```bash
cd /home/ubuntu/magazia_back
source venv/bin/activate
git pull  # if using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## Security Checklist

- [ ] Generated new SECRET_KEY for production
- [ ] DEBUG = False in settings.py (already configured)
- [ ] ALLOWED_HOSTS properly configured (already configured)
- [ ] Database using strong password
- [ ] Firewall configured (UFW)
- [ ] SSL certificate installed
- [ ] Regular backups configured for database
- [ ] EC2 Security Group allows only necessary ports (22, 80, 443)
- [ ] MySQL root password secured
- [ ] MySQL remote access disabled (default)

## Monitoring and Maintenance

### Database Backups
```bash
# Manual backup
mysqldump -uallsy_user -p allsy > backup_$(date +%Y%m%d).sql

# Backup with timestamp to specific directory
mkdir -p /home/ubuntu/backups
mysqldump -uallsy_user -pMarganeci123! allsy > /home/ubuntu/backups/allsy_backup_$(date +%Y%m%d_%H%M%S).sql
```

### Automated Daily Backups (Recommended)
Create a cron job for daily backups:
```bash
# Edit crontab
crontab -e

# Add this line for daily backup at 2 AM
0 2 * * * /usr/bin/mysqldump -uallsy_user -pMarganeci123! allsy > /home/ubuntu/backups/allsy_backup_$(date +\%Y\%m\%d).sql 2>> /home/ubuntu/backups/backup.log

# Keep only last 7 days of backups
0 3 * * * find /home/ubuntu/backups -name "allsy_backup_*.sql" -mtime +7 -delete
```

### Restore from Backup
```bash
mysql -uallsy_user -pMarganeci123! allsy < backup_file.sql
```

### Monitor Disk Space
```bash
df -h
```

### Monitor Memory Usage
```bash
free -h
```

### Monitor System Resources
```bash
htop
```

## Troubleshooting

### Gunicorn won't start
```bash
# Check logs
sudo journalctl -u gunicorn -n 50

# Test gunicorn manually
cd /home/ubuntu/magazia_back
source venv/bin/activate
gunicorn --config gunicorn_config.py vueshop_backend.wsgi:application
```

### 502 Bad Gateway
- Check if Gunicorn is running: `sudo systemctl status gunicorn`
- Check Gunicorn logs: `sudo journalctl -u gunicorn -f`
- Check nginx error logs: `sudo tail -f /var/log/nginx/error.log`

### Static files not loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Database connection errors
- Verify .env file has correct database credentials
- Check if MySQL is running: `sudo systemctl status mysql`
- Test connection: `mysql -uallsy_user -pMarganeci123! -e "USE allsy; SHOW TABLES;"`
- Check MySQL error logs: `sudo tail -f /var/log/mysql/error.log`

## Production Settings Already Configured

The following production settings are already configured in settings.py:

- WhiteNoise for serving static files
- CORS configuration for frontend domains
- MySQL local database connection
- Security middleware
- SSL/HTTPS enforcement (when DEBUG=False)
- Secure cookies
- HSTS headers
- XSS protection
- Content type sniffing protection

## Support

For issues, check:
1. Application logs: `sudo journalctl -u gunicorn -f`
2. Nginx logs: `/var/log/nginx/error.log`
3. Django debug (temporarily set DEBUG=True to see detailed errors)

## Next Steps

1. Set up monitoring (CloudWatch, New Relic, etc.)
2. Configure automated backups
3. Set up CI/CD pipeline
4. Configure log aggregation
5. Set up health checks
6. Configure auto-scaling (if needed)
