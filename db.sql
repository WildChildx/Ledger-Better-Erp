create database erp;

use erp;

create user 'dbms'@'localhost' identified by '1234';

GRANT ALL PRIVILEGES ON erp.* TO 'dbms'@'localhost';

CREATE TABLE students (
  `Roll_no` varchar(10) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `contact_no` varchar(10) DEFAULT NULL,
  `mail_id` varchar(50) DEFAULT NULL,
  `dept_name` varchar(20) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `is_admitted` tinyint(1) DEFAULT NULL
)

CREATE TABLE teacher (
  `name` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL
)

CREATE TABLE events (
  `description` varchar(600) DEFAULT NULL,
  `link` varchar(300) DEFAULT NULL
)

CREATE TABLE admin (
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL
)
