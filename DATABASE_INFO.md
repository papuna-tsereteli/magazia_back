# Database Configuration

## Local MySQL Database Setup

This project uses a **local MySQL database** on the EC2 instance instead of AWS RDS.

### Database Details

- **Database Name**: `allsy`
- **Database User**: `allsy_user`
- **Database Password**: `Marganeci123!`
- **Host**: `localhost`
- **Port**: `3306`

### Environment Configuration

The `.env` file contains:
```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=allsy
DB_USER=allsy_user
DB_PASSWORD=Marganeci123!
DB_HOST=localhost
DB_PORT=3306
```

## Setup Methods

### Option 1: Automated Setup (Recommended)
The `deploy_ec2.sh` script automatically installs and configures MySQL when you run it:
```bash
./deploy_ec2.sh
```

### Option 2: Manual Setup
Use the standalone MySQL setup script:
```bash
chmod +x setup_mysql.sh
./setup_mysql.sh
```

### Option 3: Manual Commands
```bash
# Install MySQL
sudo apt install -y mysql-server

# Start MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Create database and user
sudo mysql -e "CREATE DATABASE IF NOT EXISTS allsy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'allsy_user'@'localhost' IDENTIFIED BY 'Marganeci123!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON allsy.* TO 'allsy_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

## Database Operations

### Connect to MySQL
```bash
mysql -uallsy_user -pMarganeci123! allsy
```

### Run Django Migrations
```bash
source venv/bin/activate
python manage.py migrate
```

### Create Database Backup
```bash
mysqldump -uallsy_user -pMarganeci123! allsy > backup_$(date +%Y%m%d).sql
```

### Restore from Backup
```bash
mysql -uallsy_user -pMarganeci123! allsy < backup_file.sql
```

### Import Existing Data
If you have existing data from your local development database:

1. Export from your local machine:
```bash
mysqldump -u your_local_user -p allsy > allsy_data.sql
```

2. Upload to EC2:
```bash
scp -i your-key.pem allsy_data.sql ubuntu@63.176.47.213:/home/ubuntu/
```

3. Import on EC2:
```bash
mysql -uallsy_user -pMarganeci123! allsy < /home/ubuntu/allsy_data.sql
```

## Security Considerations

1. **Password Security**: Change the default password in production
   ```bash
   # Generate a strong password
   openssl rand -base64 32

   # Update MySQL user password
   sudo mysql -e "ALTER USER 'allsy_user'@'localhost' IDENTIFIED BY 'new_strong_password';"

   # Update .env file with new password
   ```

2. **MySQL Root Access**: Secure the MySQL root user
   ```bash
   sudo mysql_secure_installation
   ```

3. **Remote Access**: By default, MySQL only accepts local connections (secure)

4. **Regular Backups**: Set up automated backups (see EC2_DEPLOYMENT_GUIDE.md)

## Monitoring

### Check MySQL Status
```bash
sudo systemctl status mysql
```

### View MySQL Logs
```bash
sudo tail -f /var/log/mysql/error.log
```

### Check Database Size
```bash
mysql -uallsy_user -pMarganeci123! -e "
SELECT
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'allsy'
GROUP BY table_schema;"
```

### Show All Tables
```bash
mysql -uallsy_user -pMarganeci123! -e "USE allsy; SHOW TABLES;"
```

## Troubleshooting

### MySQL won't start
```bash
# Check logs
sudo tail -f /var/log/mysql/error.log

# Check disk space
df -h

# Restart MySQL
sudo systemctl restart mysql
```

### Connection refused
```bash
# Verify MySQL is running
sudo systemctl status mysql

# Check if port 3306 is listening
sudo netstat -tlnp | grep 3306

# Test connection
mysql -uallsy_user -pMarganeci123! -e "SELECT 1;"
```

### Permission denied
```bash
# Verify user permissions
sudo mysql -e "SHOW GRANTS FOR 'allsy_user'@'localhost';"

# Re-grant permissions if needed
sudo mysql -e "GRANT ALL PRIVILEGES ON allsy.* TO 'allsy_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

## Migration from RDS to Local MySQL

If you previously used AWS RDS and want to migrate to local MySQL:

1. **Backup RDS Database**:
```bash
mysqldump -h your-rds-endpoint.amazonaws.com -u admin -p database_name > rds_backup.sql
```

2. **Setup Local MySQL** (using methods above)

3. **Import RDS Data**:
```bash
mysql -uallsy_user -pMarganeci123! allsy < rds_backup.sql
```

4. **Update .env**:
```env
DB_HOST=localhost
DB_NAME=allsy
DB_USER=allsy_user
```

5. **Test Application**:
```bash
python manage.py check
python manage.py migrate
```

## Performance Tuning

For better performance, consider adjusting MySQL settings in `/etc/mysql/mysql.conf.d/mysqld.cnf`:

```ini
[mysqld]
max_connections = 200
innodb_buffer_pool_size = 1G  # Set to 70-80% of available RAM
innodb_log_file_size = 256M
query_cache_size = 64M
```

After changes, restart MySQL:
```bash
sudo systemctl restart mysql
```
