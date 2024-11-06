DROP DATABASE IF EXISTS APS;
CREATE DATABASE APS;
USE APS;

-- Table for User
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    profileImage VARCHAR DEFAULT '',
    firstName VARCHAR NOT NULL,
    lastName VARCHAR NOT NULL,
    middleName VARCHAR DEFAULT '',
    gender VARCHAR DEFAULT 'Male',
    email VARCHAR UNIQUE NOT NULL,
    is_deactivated BOOLEAN DEFAULT FALSE,
    password VARCHAR NOT NULL,
    department VARCHAR DEFAULT '',
    skills VARCHAR[] DEFAULT ARRAY[]::VARCHAR[],
    phoneNumber VARCHAR DEFAULT '',
    location VARCHAR DEFAULT '',
    position VARCHAR DEFAULT '',
    salary INTEGER DEFAULT 0,
    status VARCHAR DEFAULT 'Active',
    projectManager VARCHAR DEFAULT '',
    isManager BOOLEAN DEFAULT FALSE,
    startDate DATE DEFAULT CURRENT_DATE,
    endDate DATE DEFAULT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Project
CREATE TABLE Projects (
    id SERIAL PRIMARY KEY,
    projectManager INTEGER NOT NULL,
    projectName VARCHAR DEFAULT '',
    projectLocation VARCHAR DEFAULT '',
    projectType VARCHAR DEFAULT '',
    projectDescription VARCHAR DEFAULT '',
    startDate DATE DEFAULT NULL,
    endDate DATE DEFAULT NULL,
    projectEmployees INTEGER[] DEFAULT ARRAY[]::INTEGER[],
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_project_manager FOREIGN KEY (projectManager) REFERENCES Users(id) ON DELETE CASCADE
);

-- Setting up the one-to-many relationship
ALTER TABLE Projects
ADD CONSTRAINT fk_user_project
FOREIGN KEY (projectManager) REFERENCES Users(id) ON DELETE CASCADE;
