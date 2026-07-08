[Figma Design](https://www.figma.com/design/ZcNtiCJy8FXmMCDlMt0jrK/skill_exchange_ui?node-id=0-1&t=Hosw9T4Er5c1Y6bq-1)




# sample data

INSERT INTO users (full_name, email, password_hash, university, department, year_of_study, role, created_at, updated_at) VALUES 
('Alice Student', 'alice@university.edu', 'pbkdf2:sha256:600000$nZ8a...[hashed_password_here]', 'Tech University', 'Computer Science', 2, 'student', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Bob Mentor', 'bob@university.edu', 'pbkdf2:sha256:600000$y9wQ...[hashed_password_here]', 'Tech University', 'Computer Science', 4, 'student', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO skills (user_id, category_id, title, short_desc, description, level, session_duration, session_format, max_students, availability, topics, outcomes, status, created_at, updated_at) VALUES 
(2, 1, 'Python Programming', 'Learn Python from basics to automation', 'A comprehensive course covering data structures and web scraping.', 'Intermediate', '60 minutes', 'Both', 5, 
'["Monday 10:00-12:00", "Wednesday 14:00-16:00"]', 
'["Variables", "Loops", "Functions", "APIs"]', 
'["Build a web scraper", "Automate daily tasks"]', 
'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO users (full_name, email, password_hash, university, department, year_of_study, role, is_active, created_at, updated_at) VALUES 
('Alice Johnson', 'alice.j@uni.edu', 'pbkdf2:sha256:600000$hZ8aR9Kz$e9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2', 'Tech University', 'Computer Science', 2, 'student', True, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Bob Smith', 'bob.s@uni.edu', 'pbkdf2:sha256:600000$hZ8aR9Kz$e9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2', 'Tech University', 'Data Science', 3, 'student', True, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Charlie Davis', 'charlie.d@uni.edu', 'pbkdf2:sha256:600000$hZ8aR9Kz$e9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2', 'State College', 'Engineering', 4, 'student', True, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Diana Prince', 'diana.p@uni.edu', 'pbkdf2:sha256:600000$hZ8aR9Kz$e9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2', 'Global Institute', 'Physics', 1, 'student', True, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Admin User', 'admin@platform.com', 'pbkdf2:sha256:600000$hZ8aR9Kz$e9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2', 'System', 'Admin', 0, 'admin', True, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


INSERT INTO skills (user_id, category_id, title, short_desc, description, level, session_duration, session_format, max_students, availability, topics, outcomes, status, created_at, updated_at) VALUES 
(1, 1, 'Advanced Python', 'Mastering OOP and Decorators', 'Deep dive into Python architecture.', 'Advanced', '60 minutes', 'Online', 3, '["Tuesday 10:00"]', '["OOP", "Decorators"]', '["Write cleaner code"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 2, 'Data Analysis with Pandas', 'Transform raw data into insights', 'Learn to clean and manipulate datasets.', 'Intermediate', '90 minutes', 'Both', 10, '["Friday 14:00"]', '["Pandas", "NumPy"]', '["Generate reports"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 3, 'Public Speaking 101', 'Overcome stage fright', 'Techniques for confident presentations.', 'Beginner', '45 minutes', 'In-person', 5, '["Saturday 11:00"]', '["Body language", "Tone"]', '["Present confidently"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 1, 'SQL Databases', 'Querying like a pro', 'Master Joins, Subqueries, and Indexes.', 'Intermediate', '60 minutes', 'Both', 4, '["Monday 09:00"]', '["Joins", "Aggregation"]', '["Optimize queries"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 4, 'Time Management', 'Master your schedule', 'Proven frameworks for productivity.', 'Beginner', '30 minutes', 'Online', 20, '["Wednesday 16:00"]', '["Pomodoro", "Eisenhower"]', '["Better focus"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 5, 'Emotional Intelligence', 'Navigate social dynamics', 'Understanding self and others.', 'Intermediate', '60 minutes', 'In-person', 8, '["Thursday 13:00"]', '["Empathy", "Self-awareness"]', '["Better leadership"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 2, 'Machine Learning Basics', 'Intro to Scikit-Learn', 'Classification and Regression.', 'Advanced', '120 minutes', 'Online', 2, '["Sunday 10:00"]', '["Models", "Training"]', '["Predict outcomes"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 3, 'Technical Writing', 'Docs for developers', 'Writing API docs and tutorials.', 'Intermediate', '45 minutes', 'Online', 6, '["Tuesday 17:00"]', '["Structuring", "Audience"]', '["Clearer manuals"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 5, 'Conflict Resolution', 'Navigating disagreements', 'Conflict de-escalation strategies.', 'Intermediate', '60 minutes', 'In-person', 4, '["Friday 15:00"]', '["Negotiation", "Mediation"]', '["Peaceful resolution"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 4, 'Strategic Planning', 'Long-term goal setting', 'Aligning resources with vision.', 'Advanced', '90 minutes', 'Both', 3, '["Monday 11:00"]', '["Goal setting", "SWOT"]', '["Roadmap creation"]', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
-- (Repeat pattern for remaining 40 entries with varied topics and skill levels...)
