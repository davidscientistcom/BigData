-- Inicialización de la base de datos para monitorización (Stack Grafana)
-- Crea tabla de clientes y datos de ejemplo

CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

CREATE TABLE IF NOT EXISTS clients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO clients (name, email) VALUES
('Cliente A','a@example.com'),
('Cliente B','b@example.com')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Usuario para el mysqld_exporter (usado por prom/mysqld-exporter)
CREATE USER IF NOT EXISTS 'exporter'@'%' IDENTIFIED BY 'exporter_pass';
GRANT PROCESS, REPLICATION CLIENT, SELECT ON performance_schema.* TO 'exporter'@'%';
FLUSH PRIVILEGES;
