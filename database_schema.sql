-- Database Schema for Label Generator Application
-- Execute this script in your MySQL database

CREATE DATABASE IF NOT EXISTS label_generator_db;
USE label_generator_db;

-- Table for users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    approved_by INT NULL,
    approved_at TIMESTAMP NULL,
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Table for application settings
CREATE TABLE app_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for generated labels
CREATE TABLE labels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,

    -- Sender information
    sender_name VARCHAR(100) NOT NULL,
    sender_address TEXT NOT NULL,
    sender_city VARCHAR(50) NOT NULL,
    sender_state VARCHAR(50) NOT NULL,
    sender_zip VARCHAR(20) NOT NULL,

    -- Recipient information
    recipient_name VARCHAR(100) NOT NULL,
    recipient_address TEXT NOT NULL,
    recipient_city VARCHAR(50) NOT NULL,
    recipient_state VARCHAR(50) NOT NULL,
    recipient_zip VARCHAR(20) NOT NULL,
    recipient_tracking VARCHAR(100) NULL,

    -- Label metadata
    label_type VARCHAR(50) DEFAULT 'standard',
    status VARCHAR(20) DEFAULT 'generated',
    notes TEXT NULL,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_tracking (recipient_tracking),
    INDEX idx_created_at (created_at)
);

-- Table for audit log
CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
);

-- Insert default admin user (password: 'admin123')
INSERT INTO users (username, email, password_hash, full_name, is_active, is_admin)
VALUES ('admin', 'admin@labelgenerator.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/iwO.O3/nI7eSRnNXi', 'Administrator', TRUE, TRUE);

-- Insert default application settings
INSERT INTO app_settings (setting_key, setting_value, description) VALUES
('google_api_enabled', 'false', 'Enable Google Places API for address autocomplete'),
('google_api_key', '', 'Google Maps API Key for address autocomplete'),
('auto_approve_users', 'false', 'Automatically approve new user registrations'),
('max_labels_per_day', '100', 'Maximum labels a user can generate per day'),
('require_tracking', 'false', 'Make tracking number required for all labels');

-- Create indexes for better performance
CREATE INDEX idx_labels_date ON labels (created_at DESC);
CREATE INDEX idx_users_active ON users (is_active);
CREATE INDEX idx_settings_key ON app_settings (setting_key);