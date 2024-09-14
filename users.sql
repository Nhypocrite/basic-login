CREATE DATABASE IF NOT EXISTS web_programming;

USE web_programming;

-- Create users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL  -- SHA-256 hashed encryped data
);

