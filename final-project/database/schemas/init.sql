-- Create database
CREATE DATABASE devops_db;

-- Connect to database
\c devops_db

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on title for faster queries
CREATE INDEX idx_tasks_title ON tasks(title);

-- Insert sample data
INSERT INTO tasks (title, description, completed) VALUES
('Learn Kubernetes', 'Master container orchestration', FALSE),
('Setup CI/CD Pipeline', 'Configure GitHub Actions', FALSE),
('Deploy Application', 'Deploy to production cluster', FALSE),
('Write Documentation', 'Complete project documentation', TRUE),
('Review Code', 'Code review for team members', FALSE);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();
