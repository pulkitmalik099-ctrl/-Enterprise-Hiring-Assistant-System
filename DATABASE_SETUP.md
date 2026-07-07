# Local Database Setup Guide

## Quick Setup (Recommended)

### Option 1: Automated Setup (Easiest)

```bash
# Run the automated setup script
local-db-setup.bat
```

This will:
1. ✅ Check Docker installation
2. ✅ Start PostgreSQL container
3. ✅ Start Redis container
4. ✅ Initialize database schema
5. ✅ Insert sample data
6. ✅ Display connection information

**Time**: ~30 seconds

---

## Manual Setup

### Prerequisites

- **Docker Desktop** - Download from https://www.docker.com/products/docker-desktop
- **Docker running** - Must be running before executing commands

### Step 1: Start PostgreSQL

```bash
docker run -d ^
    --name hiring-postgres ^
    -e POSTGRES_USER=hiring_user ^
    -e POSTGRES_PASSWORD=hiring_password ^
    -e POSTGRES_DB=hiring_db ^
    -p 5432:5432 ^
    -v postgres_data:/var/lib/postgresql/data ^
    postgres:15
```

**Verify:**
```bash
docker logs hiring-postgres
```

### Step 2: Start Redis

```bash
docker run -d ^
    --name hiring-redis ^
    -p 6379:6379 ^
    redis:7
```

**Verify:**
```bash
docker logs hiring-redis
```

### Step 3: Initialize Database

```bash
# Open PostgreSQL CLI
docker exec -it hiring-postgres psql -U hiring_user -d hiring_db

# Paste the contents of db/init.sql
# Or run from file:
docker exec -i hiring-postgres psql -U hiring_user -d hiring_db < db/init.sql
```

### Step 4: Insert Sample Data

```bash
docker exec -i hiring-postgres psql -U hiring_user -d hiring_db < db/sample-data.sql
```

---

## Connection Information

### PostgreSQL
```
Host:     localhost
Port:     5432
User:     hiring_user
Password: hiring_password
Database: hiring_db
URL:      postgresql://hiring_user:hiring_password@localhost:5432/hiring_db
```

### Redis
```
Host:     localhost
Port:     6379
Password: (none)
URL:      redis://localhost:6379/0
```

---

## Database Access

### PostgreSQL Command Line

```bash
# Access PostgreSQL CLI
docker exec -it hiring-postgres psql -U hiring_user -d hiring_db

# Useful commands in psql:
\dt                  # List all tables
\d candidates        # Describe candidates table
\d job_requisitions  # Describe jobs table
SELECT * FROM candidates;    # View all candidates
SELECT * FROM job_requisitions;  # View all jobs
\q                   # Exit
```

### Redis Command Line

```bash
# Access Redis CLI
docker exec -it hiring-redis redis-cli

# Useful commands:
KEYS *               # List all keys
GET key_name         # Get value
DEL key_name         # Delete key
FLUSHDB              # Clear all data
EXIT                 # Exit
```

### Using Database Tools

You can also use GUI tools to connect:

**DBeaver (PostgreSQL)**
- Download: https://dbeaver.io/
- Connection:
  - Host: localhost
  - Port: 5432
  - Username: hiring_user
  - Password: hiring_password
  - Database: hiring_db

**Redis Desktop Manager**
- Download: https://github.com/lework/RedisDesktopManager
- Connection:
  - Host: localhost
  - Port: 6379

---

## Database Schema

### Candidates Table

```sql
CREATE TABLE candidates (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    location VARCHAR(255),
    resume_text TEXT NOT NULL,
    resume_url VARCHAR(500),
    parsed_data JSONB,           -- AI analysis results
    job_matches JSONB,           -- Job matching results
    interview_prep JSONB,        -- Interview preparation
    feedback JSONB,              -- Interview feedback
    salary_analysis JSONB,       -- Salary analysis
    status VARCHAR(50),          -- submitted, reviewed, shortlisted, interviewed, offered, rejected
    quality_score FLOAT,         -- 0-100 score
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Job Requisitions Table

```sql
CREATE TABLE job_requisitions (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    required_skills JSONB,       -- Array of required skills
    nice_to_have_skills JSONB,   -- Array of optional skills
    required_experience_years INTEGER,
    location VARCHAR(255),
    salary_range_min FLOAT,
    salary_range_max FLOAT,
    department VARCHAR(255),
    status VARCHAR(50),          -- open, closed, filled, cancelled
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Sample Queries

```sql
-- Find all candidates
SELECT * FROM candidates;

-- Find candidates by status
SELECT * FROM candidates WHERE status = 'shortlisted';

-- Find open jobs
SELECT * FROM job_requisitions WHERE status = 'open';

-- Find jobs by department
SELECT * FROM job_requisitions WHERE department = 'Engineering';

-- Count candidates by status
SELECT status, COUNT(*) FROM candidates GROUP BY status;

-- Find high-quality resumes
SELECT name, email, quality_score FROM candidates WHERE quality_score > 80;

-- Jobs with salary info
SELECT title, salary_range_min, salary_range_max FROM job_requisitions WHERE status = 'open';
```

---

## Docker Container Management

### View Containers

```bash
# See running containers
docker ps

# See all containers (including stopped)
docker ps -a

# View container details
docker inspect hiring-postgres
docker inspect hiring-redis
```

### Container Logs

```bash
# View PostgreSQL logs
docker logs hiring-postgres

# View Redis logs
docker logs hiring-redis

# Stream logs in real-time
docker logs -f hiring-postgres
docker logs -f hiring-redis
```

### Start/Stop Containers

```bash
# Stop containers
docker stop hiring-postgres hiring-redis

# Start containers
docker start hiring-postgres hiring-redis

# Restart containers
docker restart hiring-postgres hiring-redis

# Remove containers
docker rm hiring-postgres hiring-redis
```

### Backup Data

```bash
# Backup PostgreSQL database
docker exec hiring-postgres pg_dump -U hiring_user hiring_db > backup.sql

# Restore from backup
docker exec -i hiring-postgres psql -U hiring_user hiring_db < backup.sql

# Backup all volumes
docker run --rm -v postgres_data:/data -v %cd%:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find what's using port 5432
netstat -ano | findstr :5432

# Kill the process
taskkill /PID <PID> /F

# Or use different port
docker run -d -p 5433:5432 --name hiring-postgres-alt postgres:15
```

### Container Won't Start

```bash
# Check logs
docker logs hiring-postgres

# Remove old container and data
docker rm hiring-postgres
docker volume rm postgres_data

# Try again
local-db-setup.bat
```

### Can't Connect to Database

**Verify Docker is running:**
```bash
docker ps
```

**Verify containers are running:**
```bash
docker ps | findstr hiring-postgres
docker ps | findstr hiring-redis
```

**Verify connection string:**
```bash
# In Python
DATABASE_URL = "postgresql://hiring_user:hiring_password@localhost:5432/hiring_db"

# In .env file
DATABASE_URL=postgresql://hiring_user:hiring_password@localhost:5432/hiring_db
```

**Test connection:**
```bash
# Using psql
docker exec hiring-postgres psql -U hiring_user -d hiring_db -c "SELECT 1"

# Using Redis CLI
docker exec hiring-redis redis-cli ping
```

---

## Cleanup

### Remove Everything

```bash
# Stop containers
docker stop hiring-postgres hiring-redis

# Remove containers
docker rm hiring-postgres hiring-redis

# Remove volumes (data)
docker volume rm postgres_data

# Or use the cleanup script
local-db-cleanup.bat
```

---

## Environment Variables

Create `.env` file in project root:

```env
# Database
DATABASE_URL=postgresql://hiring_user:hiring_password@localhost:5432/hiring_db
DATABASE_ECHO=False

# Cache
REDIS_URL=redis://localhost:6379/0

# LLM APIs
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here

# Application
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
```

---

## Integration with Application

### Python (FastAPI)

Update `app/config.py` with local credentials:

```python
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://hiring_user:hiring_password@localhost:5432/hiring_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    ...
```

### Docker Compose (Alternative)

Instead of manual setup, use `docker-compose.yml`:

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

---

## Performance Tips

### PostgreSQL

```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM candidates WHERE status = 'shortlisted';

-- Check missing indexes
SELECT schemaname, tablename, indexname FROM pg_indexes WHERE schemaname = 'public';

-- Vacuum database (optimize)
VACUUM ANALYZE;
```

### Redis

```bash
# Clear cache
docker exec hiring-redis redis-cli FLUSHDB

# Monitor cache usage
docker exec hiring-redis redis-cli INFO memory

# Set key expiration
docker exec hiring-redis redis-cli SET key_name value_here EX 3600
```

---

## Useful Commands

```bash
# Start everything at once
local-db-setup.bat

# Connect to PostgreSQL
docker exec -it hiring-postgres psql -U hiring_user -d hiring_db

# Connect to Redis
docker exec -it hiring-redis redis-cli

# View all containers
docker ps -a

# Stop everything
docker stop hiring-postgres hiring-redis

# Clean up everything
local-db-cleanup.bat
```

---

## Next Steps

After database setup:

1. ✅ Update `.env` with your database credentials
2. ✅ Run the application: `run.bat`
3. ✅ Access API: http://localhost:8000
4. ✅ Check API docs: http://localhost:8000/api/docs
5. ✅ Access frontend: http://localhost:3000

---

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Docker Documentation](https://docs.docker.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Happy Development!** 🚀

For issues, check the logs:
```bash
docker logs hiring-postgres
docker logs hiring-redis
```
