-- Connect to the default database (usually 'postgres')
\c postgres

-- Create the scribblr database
CREATE DATABASE scribblr;

-- Connect to the scribblr database
\c scribblr

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create drawings table
CREATE TABLE drawings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    image_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create predictions table
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    drawing_id INTEGER REFERENCES drawings(id),
    prediction VARCHAR(255) NOT NULL,
    confidence FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX idx_drawings_user_id ON drawings(user_id);
CREATE INDEX idx_predictions_drawing_id ON predictions(drawing_id);