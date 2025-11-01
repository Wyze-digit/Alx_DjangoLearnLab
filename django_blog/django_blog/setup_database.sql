CREATE DATABASE django_blog_db;
CREATE USER blog_user WITH PASSWORD 'blog_password_123';
GRANT ALL PRIVILEGES ON DATABASE django_blog_db TO blog_user;
\c django_blog_db;
GRANT ALL ON SCHEMA public TO blog_user;

