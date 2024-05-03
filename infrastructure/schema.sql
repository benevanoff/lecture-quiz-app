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
    lecture_problemsetid INT NOT NULL,
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
    problemset_problemid INT NOT NULL,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS `users`;
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    username VARCHAR(255) NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    type ENUM('student', 'teacher', 'admin') NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX lecture_id ON lectures (lecture_id);
CREATE UNIQUE INDEX problemset_id ON problemsets (problemset_id);
CREATE UNIQUE INDEX problem_id ON problems (problem_id);
CREATE UNIQUE INDEX username ON users (username);
