CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    summary VARCHAR,
    status VARCHAR NOT NULL DEFAULT 'draft',
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Password for all users: password123
INSERT INTO users (email, username, first_name, last_name, hashed_password, role) VALUES
('admin@example.com', 'admin', 'Admin', 'User', '$2b$12$6WhM.e8wo2RfKJCQ.lW5wOrWGc4K9bl1Zse78rFWqGmiy.bvSZXqC', 'admin'),
('editor@example.com', 'editor', 'Editor', 'User', '$2b$12$6WhM.e8wo2RfKJCQ.lW5wOrWGc4K9bl1Zse78rFWqGmiy.bvSZXqC', 'editor'),
('user@example.com', 'regular', 'Regular', 'User', '$2b$12$6WhM.e8wo2RfKJCQ.lW5wOrWGc4K9bl1Zse78rFWqGmiy.bvSZXqC', 'user');

INSERT INTO articles (title, content, summary, status, owner_id) VALUES
('Getting Started with FastAPI', 'FastAPI is a modern, fast web framework for building APIs with Python. It is designed to be easy to use while providing high performance.', 'Introduction to FastAPI framework', 'published', 1),
('Database Design Patterns', 'When designing databases, there are several patterns to consider. Normalization, denormalization, and indexing strategies all play important roles.', 'Common patterns for database design', 'published', 2),
('My First Article', 'This is my first article on the platform. Hello world! I am excited to start sharing my knowledge.', 'A hello world article', 'published', 3),
('Draft: Advanced SQLAlchemy', 'SQLAlchemy provides powerful tools for working with databases. The ORM layer allows you to work with Python objects instead of raw SQL.', 'Deep dive into SQLAlchemy ORM', 'draft', 1),
('Python Best Practices', 'Writing clean Python code requires following certain conventions. PEP 8, type hints, and proper project structure are essential.', 'Tips for clean Python code', 'published', 2);
