DROP DATABASE IF EXISTS web_app_DB;

CREATE DATABASE IF NOT EXISTS web_app_DB;
CREATE USER IF NOT EXISTS 'web_app_user'@'localhost' identified by 'pass';
GRANT ALL PRIVILEGES ON web_app_DB.* TO 'web_app_user'@'localhost';
FLUSH PRIVILEGES;