-- Usuario de solo lectura (Power BI)
CREATE USER IF NOT EXISTS 'read_only_user'@'%' IDENTIFIED BY 'REPLACE_WITH_PASSWORD1';
GRANT SELECT ON SematecPlataform.* TO 'read_only_user'@'%';

-- Usuario de lectura y escritura (ETL, aplicaciones)
CREATE USER IF NOT EXISTS 'read_write_user'@'%' IDENTIFIED BY 'REPLACE_WITH_PASSWORD2';
GRANT SELECT, INSERT, UPDATE, DELETE ON SematecPlataform.* TO 'read_write_user'@'%';

-- Aplicar los cambios
FLUSH PRIVILEGES;
