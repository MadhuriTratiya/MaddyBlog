-- Create the login at the server level if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'MTBlogUser')
BEGIN
    CREATE LOGIN MTBlogUser WITH PASSWORD = 'MTBlogPass123!', CHECK_POLICY = OFF;
END
ELSE
BEGIN
    ALTER LOGIN MTBlogUser WITH PASSWORD = 'MTBlogPass123!';
END

-- Assign permissions for your specific blog database
USE MTBlogDB;
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'MTBlogUser')
BEGIN
    CREATE USER MTBlogUser FOR LOGIN MTBlogUser;
END
ALTER ROLE db_owner ADD MEMBER MTBlogUser;