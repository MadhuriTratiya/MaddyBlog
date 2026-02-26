CREATE DATABASE MTBlogDB;

-- 1. Create the login for the whole server
CREATE LOGIN MTBlogUser WITH PASSWORD = 'MTBlogPass123!';

-- 2. Switch to your new database
USE MTBlogDB;

-- 3. Create a user in this database for that login
CREATE USER MTBlogUser FOR LOGIN MTBlogUser;

-- 4. Give that user full control to create tables (essential for migrations)
ALTER ROLE db_owner ADD MEMBER MTBlogUser;

USE MTBlogDB;
GO

-- If the user doesn't exist, create it
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'MTBlogUser')
BEGIN
    CREATE USER MTBlogUser FOR LOGIN MTBlogUser;
END

-- Give the user owner rights so it can create tables
ALTER ROLE db_owner ADD MEMBER MTBlogUser;
GO