@echo off
REM Local Database Setup Script for Enterprise Hiring Assistant
REM This script sets up PostgreSQL and Redis for local development

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Local Database Setup
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1] Checking Docker...
docker --version
echo [✓] Docker is ready

echo.
echo [2] Starting PostgreSQL container...
docker run -d ^
    --name hiring-postgres ^
    -e POSTGRES_USER=hiring_user ^
    -e POSTGRES_PASSWORD=hiring_password ^
    -e POSTGRES_DB=hiring_db ^
    -p 5432:5432 ^
    -v postgres_data:/var/lib/postgresql/data ^
    postgres:15

if errorlevel 1 (
    echo [!] PostgreSQL might already be running...
    docker start hiring-postgres 2>nul || (
        echo [ERROR] Failed to start PostgreSQL
        pause
        exit /b 1
    )
) else (
    echo [*] Waiting for PostgreSQL to be ready...
    timeout /t 3 /nobreak
)

echo [✓] PostgreSQL is ready
echo    Host: localhost
echo    Port: 5432
echo    User: hiring_user
echo    Password: hiring_password
echo    Database: hiring_db

echo.
echo [3] Starting Redis container...
docker run -d ^
    --name hiring-redis ^
    -p 6379:6379 ^
    redis:7

if errorlevel 1 (
    echo [!] Redis might already be running...
    docker start hiring-redis 2>nul || (
        echo [ERROR] Failed to start Redis
        pause
        exit /b 1
    )
) else (
    echo [*] Waiting for Redis to be ready...
    timeout /t 2 /nobreak
)

echo [✓] Redis is ready
echo    Host: localhost
echo    Port: 6379
echo    No password

echo.
echo [4] Initializing database schema...

REM Create database initialization script
echo Creating database initialization script...

docker exec -i hiring-postgres psql -U hiring_user -d hiring_db << EOF
-- Create candidates table
CREATE TABLE IF NOT EXISTS candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    location VARCHAR(255),
    resume_text TEXT NOT NULL,
    resume_url VARCHAR(500),
    parsed_data JSONB,
    job_matches JSONB,
    interview_prep JSONB,
    feedback JSONB,
    salary_analysis JSONB,
    status VARCHAR(50) DEFAULT 'submitted',
    quality_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create jobs table
CREATE TABLE IF NOT EXISTS job_requisitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    required_skills JSONB,
    nice_to_have_skills JSONB,
    required_experience_years INTEGER,
    location VARCHAR(255),
    salary_range_min FLOAT,
    salary_range_max FLOAT,
    department VARCHAR(255),
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email);
CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON job_requisitions(status);
CREATE INDEX IF NOT EXISTS idx_jobs_department ON job_requisitions(department);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hiring_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hiring_user;
EOF

if errorlevel 1 (
    echo [!] Warning: Database initialization had issues
    echo    Continuing anyway...
) else (
    echo [✓] Database schema created
)

echo.
echo [5] Inserting sample data...

docker exec -i hiring-postgres psql -U hiring_user -d hiring_db << EOF
-- Insert sample candidates
INSERT INTO candidates (name, email, phone, location, resume_text, status) VALUES
('John Smith', 'john.smith@example.com', '555-0101', 'New York, NY', 'Senior Software Engineer with 8+ years of experience in Python and AWS.', 'submitted'),
('Sarah Johnson', 'sarah.johnson@example.com', '555-0102', 'San Francisco, CA', 'Full-stack developer with React and Node.js expertise. 6 years experience.', 'reviewed'),
('Mike Chen', 'mike.chen@example.com', '555-0103', 'Austin, TX', 'DevOps engineer with Kubernetes and Docker expertise. 10+ years in infrastructure.', 'shortlisted')
ON CONFLICT (email) DO NOTHING;

-- Insert sample jobs
INSERT INTO job_requisitions (title, description, required_skills, location, salary_range_min, salary_range_max, department, status) VALUES
('Senior Backend Engineer', 'Looking for experienced backend engineer proficient in Python and FastAPI', '["Python", "FastAPI", "PostgreSQL", "Docker"]', 'San Francisco, CA', 150000, 200000, 'Engineering', 'open'),
('Frontend Developer', 'React specialist needed for modern web application development', '["React", "JavaScript", "CSS", "TypeScript"]', 'New York, NY', 120000, 160000, 'Engineering', 'open'),
('DevOps Engineer', 'Kubernetes and cloud infrastructure expert for scaling our platform', '["Kubernetes", "AWS", "Docker", "Terraform"]', 'Remote', 140000, 190000, 'Infrastructure', 'open')
ON CONFLICT DO NOTHING;
EOF

if errorlevel 1 (
    echo [!] Warning: Sample data insertion had issues
) else (
    echo [✓] Sample data inserted
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo PostgreSQL Connection String:
echo   postgresql://hiring_user:hiring_password@localhost:5432/hiring_db
echo.
echo Redis Connection String:
echo   redis://localhost:6379/0
echo.
echo Docker Containers:
docker ps --filter "name=hiring-" --format "table {{.Names}}\t{{.Status}}"
echo.
echo Useful Docker Commands:
echo   docker logs hiring-postgres          (View PostgreSQL logs)
echo   docker logs hiring-redis             (View Redis logs)
echo   docker stop hiring-postgres hiring-redis    (Stop containers)
echo   docker start hiring-postgres hiring-redis   (Start containers)
echo   docker rm hiring-postgres hiring-redis      (Remove containers)
echo.
echo PostgreSQL CLI Access:
echo   docker exec -it hiring-postgres psql -U hiring_user -d hiring_db
echo.
echo Redis CLI Access:
echo   docker exec -it hiring-redis redis-cli
echo.
echo You can now start the application with:
echo   run.bat
echo.

pause
