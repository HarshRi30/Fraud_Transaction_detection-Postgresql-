--Creating all the Tales used in the Project

-- 1. USERS TABLE
CREATE TABLE Users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP,
    is_active BOOLEAN
);

-- 2. DEVICES TABLE
CREATE TABLE Devices (
    device_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    device_type VARCHAR(50),
    os VARCHAR(50),
    last_active TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- 3. TRANSACTIONS TABLE
CREATE TABLE Transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    device_id VARCHAR(50), -- No FK constraint here to allow 'Unknown Devices'
    transaction_date TIMESTAMP,
    amount DECIMAL(10, 2),
    merchant VARCHAR(100),
    category VARCHAR(50),
    city VARCHAR(50),
    country VARCHAR(50),
    is_fraud BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- 4. ALERTS TABLE
CREATE TABLE Alerts (
    alert_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    alert_type VARCHAR(50),
    severity VARCHAR(20),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id)
);