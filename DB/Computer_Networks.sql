CREATE DATABASE CN_PROJECT;

USE CN_PROJECT;

CREATE TABLE USERS (
    user_id          INT AUTO_INCREMENT PRIMARY KEY,
    full_name       VARCHAR(100) NOT NULL,
    username        VARCHAR(50) UNIQUE NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL, -- bycrypt 
    phone_number    VARCHAR(20) UNIQUE, -- Maybe OTP
    profile_picture VARCHAR(255),  -- URL or file path
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account_verified BOOLEAN DEFAULT FALSE  -- Indicates if email/phone verification is done
);

SELECT * FROM USERS;