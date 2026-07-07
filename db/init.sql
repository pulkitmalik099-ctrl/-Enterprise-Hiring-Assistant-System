-- Enterprise Hiring Assistant Database Initialization
-- PostgreSQL Schema and Tables

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT status_check CHECK (status IN ('submitted', 'reviewed', 'shortlisted', 'interviewed', 'offered', 'rejected'))
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT salary_check CHECK (salary_range_min < salary_range_max OR salary_range_max IS NULL),
    CONSTRAINT experience_check CHECK (required_experience_years >= 0)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email);
CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);
CREATE INDEX IF NOT EXISTS idx_candidates_created_at ON candidates(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON job_requisitions(status);
CREATE INDEX IF NOT EXISTS idx_jobs_department ON job_requisitions(department);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON job_requisitions(created_at DESC);

-- Create audit table (optional, for tracking changes)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT action_check CHECK (action IN ('INSERT', 'UPDATE', 'DELETE'))
);

CREATE INDEX IF NOT EXISTS idx_audit_table_name ON audit_log(table_name);
CREATE INDEX IF NOT EXISTS idx_audit_record_id ON audit_log(record_id);
CREATE INDEX IF NOT EXISTS idx_audit_changed_at ON audit_log(changed_at DESC);

-- Grant permissions to hiring_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hiring_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hiring_user;
GRANT USAGE ON SCHEMA public TO hiring_user;

-- Add comments for documentation
COMMENT ON TABLE candidates IS 'Stores candidate information and AI analysis results';
COMMENT ON TABLE job_requisitions IS 'Stores job openings and requirements';
COMMENT ON TABLE audit_log IS 'Audit trail for database changes';

COMMENT ON COLUMN candidates.status IS 'Hiring status: submitted, reviewed, shortlisted, interviewed, offered, rejected';
COMMENT ON COLUMN candidates.quality_score IS 'Resume quality score (0-100) based on completeness';
COMMENT ON COLUMN candidates.parsed_data IS 'Extracted resume data (JSON): skills, experience, education, etc.';

COMMENT ON COLUMN job_requisitions.status IS 'Job status: open, closed, filled, cancelled';
COMMENT ON COLUMN job_requisitions.required_skills IS 'Array of required technical skills';
COMMENT ON COLUMN job_requisitions.nice_to_have_skills IS 'Array of optional nice-to-have skills';

-- Commit
COMMIT;
