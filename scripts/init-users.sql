-- Usuario de solo lectura (Power BI)
CREATE USER IF NOT EXISTS 'read_only_user'@'%' IDENTIFIED BY 'readonly_password';
GRANT SELECT ON plataforma.* TO 'readonly_user'@'%';

-- Usuario de lectura y escritura (ETL, aplicaciones)
CREATE USER IF NOT EXISTS 'read_write_user'@'%' IDENTIFIED BY 'readwrite_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON plataforma.* TO 'readwrite_user'@'%';

-- Aplicar los cambios
FLUSH PRIVILEGES;
