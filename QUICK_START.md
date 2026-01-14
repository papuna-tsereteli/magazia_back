# Quick Start Guide - EC2 Deployment

## Fast Track Deployment (5 minutes)

### 1. Upload Project to EC2
```bash
# From your local machine
scp -i your-key.pem -r C:\Users\paguna\Desktop\magazia_back ubuntu@63.176.47.213:/home/ubuntu/
```

### 2. SSH into EC2
```bash
ssh -i your-key.pem ubuntu@63.176.47.213
```

### 3. Run Automated Deployment Script
```bash
cd /home/ubuntu/magazia_back
chmod +x deploy_ec2.sh
./deploy_ec2.sh
```

### 4. Create Admin User (Optional)
```bash
source venv/bin/activate
python manage.py createsuperuser
```

### 5. Set Up SSL Certificate
```bash
sudo certbot --nginx -d api.allsy.ge
```

### Done!

Your API should now be accessible at:
- HTTP: http://63.176.47.213
- HTTPS: https://api.allsy.ge (after SSL setup)

## What Was Configured

### Production Settings
- DEBUG = False
- WhiteNoise for static files
- MySQL local database (allsy)
- CORS for frontend domains
- Security middleware (SSL, HSTS, etc.)

### Server Stack
- MySQL Server (local database)
- Gunicorn (WSGI server)
- Nginx (reverse proxy)
- Systemd services (auto-restart)

### Files Created
1. `gunicorn_config.py` - Gunicorn settings
2. `gunicorn.service` - Systemd service
3. `nginx.conf` - Nginx configuration
4. `deploy_ec2.sh` - Automated deployment
5. `setup_mysql.sh` - MySQL setup script
6. `EC2_DEPLOYMENT_GUIDE.md` - Full documentation

## Quick Commands

### Restart Application
```bash
sudo systemctl restart gunicorn
```

### View Logs
```bash
sudo journalctl -u gunicorn -f
```

### Update Code
```bash
cd /home/ubuntu/magazia_back
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## Verify Deployment

```bash
# Check services
sudo systemctl status gunicorn
sudo systemctl status nginx

# Test API
curl http://localhost:8000
curl http://63.176.47.213
```

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u gunicorn -n 50
```

### Static files missing
```bash
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn nginx
```

For detailed documentation, see `EC2_DEPLOYMENT_GUIDE.md`
