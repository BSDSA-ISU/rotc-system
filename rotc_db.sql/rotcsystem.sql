-- =========================================
-- ROTC COMMAND CENTER DATABASE
-- =========================================

CREATE DATABASE IF NOT EXISTS rotc_db;
USE rotc_db;

-- =========================================
-- FOREIGN KEY RESET
-- =========================================

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS team_members;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- =========================================
-- USERS TABLE
-- =========================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    role VARCHAR(20) DEFAULT 'cadet',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- DEFAULT ADMIN ACCOUNT
-- =========================================

INSERT INTO users (username, password, role)
VALUES ('admin', 'koishi', 'admin');

-- =========================================
-- ATTENDANCE TABLE
-- =========================================

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    rank VARCHAR(50) NOT NULL,

    platoon VARCHAR(50) NOT NULL,

    status ENUM('Present', 'Late', 'Absent') NOT NULL,

    date_recorded DATE NOT NULL,

    submitted_by VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (submitted_by)
    REFERENCES users(username)
    ON DELETE SET NULL
);

-- =========================================
-- EQUIPMENT TABLE
-- =========================================

CREATE TABLE equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,

    borrower VARCHAR(100) NOT NULL,

    item VARCHAR(100) NOT NULL,

    quantity INT NOT NULL DEFAULT 1,

    borrow_date DATE NOT NULL,

    return_date DATE DEFAULT NULL,

    status ENUM('Borrowed', 'Returned') DEFAULT 'Borrowed',

    submitted_by VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (submitted_by)
    REFERENCES users(username)
    ON DELETE SET NULL
);

-- =========================================
-- TEAM MEMBERS TABLE
-- =========================================

CREATE TABLE team_members (
    id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    username VARCHAR(50),

    role VARCHAR(100),

    about_me TEXT,

    profile_image_path VARCHAR(255),

    github_link VARCHAR(255),

    facebook_link VARCHAR(255),

    accent_color VARCHAR(7) DEFAULT '#00d4ff',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SAMPLE TEAM MEMBERS
-- =========================================

INSERT INTO team_members
(
    full_name,
    username,
    role,
    about_me,
    profile_image_path,
    github_link,
    facebook_link,
    accent_color
)
VALUES 
(
"Lovelee Flomarjoy T. Madamba",
"asdfghjkl_lvlee",
"ganda lang",
"it's for me to know and it's for you to find out",
"/static/Madamba.jpg",
NULL,
"https://www.facebook.com/share/18QDHB69Wc/",
'#ff00ea'
),
(
"Nelo M. Cabab",
"Nelshima",
"core user",
"Mabait",
"/static/nelo.jpg",
NULL,
"https://www.facebook.com/share/1EFi9LAXbV/",
"#FFC0CB"
),
(
    'Adrian Intel Pil V. De Vera', 
    'Intedesu', 
    'Role model', 
    'mas mabait.', 
    '/static/intel.jpg', 
    NULL, 
    'https://www.facebook.com/AdrianIntelDeVera25', 
    '#7F00FF'
),
(
    'Mark Jhon Paul L. Pace', 
    'idgaf_pcee', 
    'Pabohat', 
    "it's all about me.", 
    '/static/pace.jpg', 
    NULL, 
    'https://www.facebook.com/mrkyohan/', 
    '#BA8E23'
);
-- =========================================
-- SAMPLE ATTENDANCE DATA
-- =========================================

INSERT INTO attendance
(name, rank, platoon, status, date_recorded, submitted_by)
VALUES

('Juan Dela Cruz', 'Cadet', 'Alpha', 'Present', '2026-05-12', 'admin'),

('Pedro Santos', 'Corporal', 'Bravo', 'Late', '2026-05-12', 'admin'),

('Maria Clara', 'Sergeant', 'Charlie', 'Absent', '2026-05-12', 'admin');

-- =========================================
-- SAMPLE EQUIPMENT DATA
-- =========================================

INSERT INTO equipment
(borrower, item, quantity, borrow_date, status, submitted_by)
VALUES

('Juan Dela Cruz', 'Helmet', 2, '2026-05-12', 'Borrowed', 'admin'),

('Pedro Santos', 'Radio', 1, '2026-05-12', 'Returned', 'admin'),

('Maria Clara', 'Boots', 1, '2026-05-12', 'Borrowed', 'admin');
-- =========================================
-- DASHBOARD ANALYTICS QUERIES
-- =========================================

-- Attendance Analytics
SELECT
    status,
    COUNT(*) AS count
FROM attendance
GROUP BY status;

-- Equipment Analytics
SELECT
    item,
    SUM(quantity) AS total
FROM equipment
GROUP BY item;

-- Total Attendance Records
SELECT
    COUNT(*) AS total_attendance
FROM attendance;

-- Total Equipment Borrowed
SELECT
    SUM(quantity) AS total_equipment
FROM equipment;

-- Total Team Members
SELECT
    COUNT(*) AS total_members
FROM team_members;