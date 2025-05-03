CREATE DATABASE IF NOT EXISTS airline_system;
USE airline_system;

CREATE TABLE passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_ref VARCHAR(20) UNIQUE,
    name VARCHAR(100),
    flight_number VARCHAR(10),
    class ENUM('economy', 'business', 'first'),
    seat_pref ENUM('none', 'window', 'aisle'),
    seat_number VARCHAR(10),
    boarding_group INT,
    checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flights (
    flight_number VARCHAR(10) PRIMARY KEY,
    origin VARCHAR(50),
    destination VARCHAR(50),
    departure_time DATETIME,
    arrival_time DATETIME,
    aircraft_type VARCHAR(50)
);

CREATE TABLE seats (
    flight_number VARCHAR(10),
    seat_number VARCHAR(10),
    class ENUM('economy', 'business', 'first'),
    location ENUM('window', 'aisle', 'middle'),
    available BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (flight_number, seat_number),
    FOREIGN KEY (flight_number) REFERENCES flights(flight_number)
);

CREATE TABLE boarding_groups (
    group_number INT PRIMARY KEY,
    group_name VARCHAR(50),
    description VARCHAR(100)
);

-- Simply add the new column
ALTER TABLE passengers 
ADD COLUMN seat_number VARCHAR(10) AFTER seat_pref;
-- If you see the column is named slightly differently (like seat_number already)
ALTER TABLE passengers 
CHANGE COLUMN seat_number seat_number VARCHAR(10);

-- Or if it's named 'seat' or similar
ALTER TABLE passengers 
CHANGE COLUMN seat_number seat_numb VARCHAR(10);
desc passengers;