DROP DATABASE IF EXISTS `sql_db`;
CREATE DATABASE sql_db;
USE sql_db;

DROP TABLE IF EXISTS `lectures`;
CREATE TABLE lectures (
    lecture_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    category ENUM('math', 'technology', 'chemistry', 'physics', 'english_language', 'french_language', 'history') NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS `problemsets`;
CREATE TABLE problemsets (
    problemset_id INT PRIMARY KEY AUTO_INCREMENT,
    lecture_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS `problems`;
CREATE TABLE problems (
    problem_id INT PRIMARY KEY AUTO_INCREMENT,
    problemset_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified DATETIME DEFAULT CURRENT_TIMESTAMP
);
