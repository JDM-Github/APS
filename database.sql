DROP DATABASE IF EXISTS APS;
CREATE DATABASE APS;
USE APS;

CREATE TABLE Users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(100)
);

INSERT INTO Users VALUE (
    "test"
);