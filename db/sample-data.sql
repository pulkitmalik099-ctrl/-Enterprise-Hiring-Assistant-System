-- Enterprise Hiring Assistant - Sample Data
-- Insert test data for local development

-- Sample Candidates
INSERT INTO candidates (name, email, phone, location, resume_text, status, quality_score) VALUES
(
    'John Smith',
    'john.smith@example.com',
    '555-0101',
    'New York, NY',
    'Senior Software Engineer with 8+ years of experience. Expert in Python, AWS, and system architecture. Led teams of 10+ engineers. Strong background in microservices and distributed systems.',
    'submitted',
    85.5
),
(
    'Sarah Johnson',
    'sarah.johnson@example.com',
    '555-0102',
    'San Francisco, CA',
    'Full-stack developer with 6 years of experience. Proficient in React, Node.js, TypeScript, and PostgreSQL. Passionate about building scalable web applications. Open source contributor.',
    'reviewed',
    78.3
),
(
    'Mike Chen',
    'mike.chen@example.com',
    '555-0103',
    'Austin, TX',
    'DevOps Engineer with 10+ years in cloud infrastructure. Expertise in Kubernetes, Docker, Terraform, and AWS. Designed infrastructure serving 1M+ daily active users.',
    'shortlisted',
    92.1
),
(
    'Emily Rodriguez',
    'emily.rodriguez@example.com',
    '555-0104',
    'Boston, MA',
    'Data Engineer with 5 years of experience. Skilled in Python, Apache Spark, and big data technologies. Optimized data pipelines reducing processing time by 60%.',
    'interviewed',
    88.7
),
(
    'James Wilson',
    'james.wilson@example.com',
    '555-0105',
    'Seattle, WA',
    'Product Manager with tech background. 7 years experience in SaaS. Led product from $0 to $5M ARR. Strong analytics and strategy skills.',
    'offered',
    81.2
),
(
    'Lisa Anderson',
    'lisa.anderson@example.com',
    '555-0106',
    'Denver, CO',
    'QA Automation Engineer with 4 years experience. Expertise in Selenium, Python, and CI/CD. Implemented automated testing reducing bugs by 45%.',
    'submitted',
    73.9
);

-- Sample Jobs
INSERT INTO job_requisitions (title, description, required_skills, nice_to_have_skills, required_experience_years, location, salary_range_min, salary_range_max, department, status) VALUES
(
    'Senior Backend Engineer',
    'We are looking for an experienced backend engineer to join our infrastructure team. You will design and implement scalable APIs, optimize database performance, and mentor junior engineers. Ideal candidate has experience with microservices architecture and cloud platforms.',
    '["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"]',
    '["Kubernetes", "GraphQL", "Redis", "Apache Spark"]',
    5,
    'San Francisco, CA',
    150000,
    200000,
    'Engineering',
    'open'
),
(
    'Frontend Developer',
    'Join our frontend team to build beautiful, responsive web applications using React. You will collaborate with designers and backend engineers to deliver seamless user experiences. This role is ideal for someone who is passionate about UI/UX and performance optimization.',
    '["React", "JavaScript", "TypeScript", "CSS", "HTML"]',
    '["Next.js", "Redux", "Tailwind CSS", "WebGL"]',
    3,
    'New York, NY',
    120000,
    160000,
    'Engineering',
    'open'
),
(
    'DevOps Engineer',
    'Help us scale our infrastructure to serve millions of users. You will manage our Kubernetes clusters, implement infrastructure as code, and improve deployment pipelines. Ideal candidate has hands-on experience with cloud platforms and container orchestration.',
    '["Kubernetes", "AWS", "Docker", "Terraform", "CI/CD"]',
    '["GCP", "Azure", "Ansible", "Prometheus", "ELK Stack"]',
    4,
    'Remote',
    140000,
    190000,
    'Infrastructure',
    'open'
),
(
    'Data Engineer',
    'Build and maintain our data infrastructure supporting analytics, machine learning, and business intelligence. You will design ETL pipelines, optimize data warehouses, and ensure data quality. This role requires expertise in big data technologies.',
    '["Python", "Apache Spark", "PostgreSQL", "Airflow", "AWS"]',
    '["Scala", "Kafka", "Snowflake", "dbt", "Data Modeling"]',
    3,
    'Remote',
    130000,
    180000,
    'Data',
    'open'
),
(
    'Full Stack Engineer',
    'We are seeking a versatile engineer who can work across our entire stack. You will contribute to both frontend and backend development, participate in architecture decisions, and help shape our technical culture.',
    '["Python", "React", "TypeScript", "PostgreSQL", "Docker"]',
    '["Kubernetes", "GraphQL", "Next.js", "AWS", "Testing"]',
    4,
    'San Francisco, CA',
    140000,
    190000,
    'Engineering',
    'open'
),
(
    'Product Manager',
    'Lead the vision and strategy for our core product. You will work with engineering, design, and business teams to define features, prioritize roadmap, and drive product adoption. Ideal candidate has experience scaling products in competitive markets.',
    '["Product Strategy", "Roadmap Planning", "Data Analysis", "User Research", "Stakeholder Management"]',
    '["Technical Background", "Growth Hacking", "Analytics", "A/B Testing"]',
    5,
    'New York, NY',
    160000,
    220000,
    'Product',
    'open'
),
(
    'Machine Learning Engineer',
    'Develop and deploy machine learning models that power our AI features. You will work on recommendation systems, natural language processing, and computer vision. Ideal candidate has experience with production ML systems.',
    '["Python", "TensorFlow", "PyTorch", "Scikit-learn", "AWS"]',
    '["Kubernetes", "MLflow", "FastAPI", "Data Pipelines", "Model Deployment"]',
    3,
    'Remote',
    150000,
    200000,
    'Engineering',
    'open'
);

-- Insert parsed data for candidates (sample AI analysis results)
UPDATE candidates SET parsed_data = '{
    "summary": "Senior engineer with strong Python and cloud expertise",
    "skills": ["Python", "FastAPI", "AWS", "Docker", "PostgreSQL", "Kubernetes"],
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "TechCorp",
            "duration": "2020-Present",
            "description": "Led infrastructure team, designed microservices architecture"
        }
    ],
    "education": [
        {
            "degree": "BS Computer Science",
            "institution": "Stanford University",
            "field": "Computer Science"
        }
    ],
    "certifications": ["AWS Solutions Architect", "Kubernetes Certified Application Developer"],
    "languages": ["English", "Mandarin"]
}'
WHERE email = 'john.smith@example.com';

UPDATE candidates SET parsed_data = '{
    "summary": "Full-stack developer with React expertise",
    "skills": ["React", "Node.js", "TypeScript", "PostgreSQL", "AWS"],
    "experience": [
        {
            "title": "Full Stack Engineer",
            "company": "StartupXYZ",
            "duration": "2019-Present",
            "description": "Built and scaled web platform from ground up"
        }
    ],
    "education": [
        {
            "degree": "BS Information Technology",
            "institution": "UC Berkeley",
            "field": "Information Technology"
        }
    ],
    "certifications": ["AWS Developer Associate"],
    "languages": ["English", "Spanish"]
}'
WHERE email = 'sarah.johnson@example.com';

-- Commit
COMMIT;
