-- ==============================================================================
-- HR ATTRITION DATA WAREHOUSE - SEEDING & DIMENSION POPULATION ETL
-- ==============================================================================

-- 1. Populate dim_department
INSERT OR IGNORE INTO dim_department (department_name, cost_center_code, division_head) VALUES
('Sales', 'CC-101-SLS', 'Chief Commercial Officer'),
('Research & Development', 'CC-202-RND', 'Chief Technology Officer'),
('Human Resources', 'CC-303-HRM', 'Chief People Officer');

-- 2. Populate dim_satisfaction_scale
INSERT OR IGNORE INTO dim_satisfaction_scale (rating_id, rating_label, sentiment_band, risk_weight) VALUES
(1, 'Low', 'Critical Dissatisfaction', 1.00),
(2, 'Medium', 'Neutral / Moderate', 0.60),
(3, 'High', 'Satisfied', 0.25),
(4, 'Very High', 'Strongly Engaged', 0.05);

-- 3. Populate dim_job_role (Standard Compensation Benchmark Grades)
INSERT OR IGNORE INTO dim_job_role (job_role_name, department_name, career_track, standard_min_salary, standard_max_salary) VALUES
('Sales Executive', 'Sales', 'Field Sales', 4000, 11000),
('Research Scientist', 'Research & Development', 'Technical / Science', 3000, 10000),
('Laboratory Technician', 'Research & Development', 'Technical Operations', 2000, 7500),
('Manufacturing Director', 'Research & Development', 'Leadership Operations', 10000, 19000),
('Healthcare Representative', 'Research & Development', 'Medical Liaison', 5000, 14000),
('Manager', 'Sales', 'General Management', 11000, 20000),
('Sales Representative', 'Sales', 'Entry Sales', 2000, 6000),
('Research Director', 'Research & Development', 'Scientific Leadership', 12000, 20000),
('Human Resources', 'Human Resources', 'People Operations', 2500, 10000);
