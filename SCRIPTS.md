# Windows Batch Scripts Guide

This directory contains convenient batch scripts to manage the Enterprise Hiring Assistant System on Windows.

## Available Scripts

### 1. **run.bat** - Start Everything
Fully automated setup and application launch.

**What it does:**
- Creates virtual environment (if needed)
- Installs dependencies
- Sets up .env configuration
- Starts Docker services (PostgreSQL, Redis)
- Launches the FastAPI application

**Usage:**
```batch
run.bat
```

**Output:**
- Application runs on `http://localhost:8000`
- API docs available at `http://localhost:8000/api/docs`
- Press `Ctrl+C` to stop

### 2. **setup.bat** - Initial Setup Only
Prepares the environment without running the application.

**What it does:**
- Creates virtual environment
- Installs dependencies
- Creates .env file from template
- Prompts to edit .env with API keys

**Usage:**
```batch
setup.bat
```

**When to use:**
- First-time setup
- Installing new dependencies
- Configuring API keys

### 3. **stop.bat** - Stop Services
Cleanly stops Docker services and containers.

**What it does:**
- Stops and removes Docker containers
- Stops database and cache services

**Usage:**
```batch
stop.bat
```

**When to use:**
- When `run.bat` is not stopping properly
- To manually stop services
- Before system shutdown

### 4. **test.bat** - Run Tests
Executes the test suite with coverage reporting.

**What it does:**
- Activates virtual environment
- Runs pytest with coverage
- Generates HTML coverage report

**Usage:**
```batch
test.bat
```

**Output:**
- Test results in terminal
- Coverage report in `htmlcov/index.html`

## Prerequisites

### Required Software
1. **Python 3.10+**
   - Download: https://www.python.org/downloads/
   - Add to PATH during installation

2. **Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop
   - Must be running before executing scripts

3. **Git** (optional, for version control)
   - Download: https://git-scm.com/

### Windows Firewall
- Allow Docker Desktop through Windows Firewall
- Allow Python through Windows Firewall

## Quick Start

### First Time Setup
```batch
REM 1. Initial setup
setup.bat

REM 2. Edit .env file with your API keys (uses Notepad)
REM    Uncomment and set:
REM    ANTHROPIC_API_KEY=your_key_here
REM    OPENAI_API_KEY=your_key_here (optional)

REM 3. Start the application
run.bat
```

### Running Again
```batch
REM Simply run:
run.bat

REM Or use a shortcut - Create a shortcut to run.bat on your desktop
```

## Configuration

### .env File
The scripts automatically create `.env` from `.env.example`. Edit it with your API keys:

```env
# Application
APP_NAME=Enterprise Hiring Assistant
DEBUG=False
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://hiring_user:hiring_password@localhost:5432/hiring_db

# LLM APIs (REQUIRED)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx (optional)

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
```

## Troubleshooting

### "Python is not installed"
```batch
REM Check if Python is in PATH
python --version

REM If not found:
REM 1. Install Python 3.10+ from https://www.python.org/
REM 2. Check "Add Python to PATH" during installation
REM 3. Restart your terminal
```

### "Docker is not installed"
```batch
REM Check if Docker is installed
docker --version

REM If not found:
REM 1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
REM 2. Start Docker Desktop
REM 3. Run the script again
```

### Port 8000 Already in Use
```batch
REM Edit run.bat, find the uvicorn line and change port:
REM Change: --port 8000
REM To: --port 8001

REM Or kill the process using the port:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Docker Services Won't Start
```batch
REM 1. Make sure Docker Desktop is running
REM 2. Check if containers exist:
docker ps -a

REM 3. Remove old containers:
docker-compose down -v

REM 4. Try again:
run.bat
```

### API Key Errors
```batch
REM 1. Edit .env file
REM 2. Verify your API keys are valid
REM 3. Ensure no extra spaces or quotes
REM 4. Restart the application
```

## Advanced Usage

### Run Specific Tests
```batch
REM Activate environment first
call venv\Scripts\activate.bat

REM Run specific test file
pytest tests/unit/test_main.py -v

REM Run with specific pattern
pytest -k "test_resume" -v

REM Run with coverage
pytest --cov=app --cov-report=html
```

### Check Application Logs
```batch
REM While app is running, check the terminal output
REM Logs appear in real-time

REM Or check Docker logs:
docker logs hiring_app
docker logs hiring_db
docker logs hiring_redis
```

### Access Database
```batch
REM Connect to PostgreSQL while services are running:
REM Use a tool like pgAdmin or DBeaver
REM 
REM Connection Details:
REM Host: localhost
REM Port: 5432
REM Username: hiring_user
REM Password: hiring_password
REM Database: hiring_db
```

## Creating Desktop Shortcuts

### Quick Start Shortcut
1. Right-click on `run.bat` → Create shortcut
2. Right-click the shortcut → Properties
3. Change "Start in" to the project directory
4. Click OK
5. Move shortcut to Desktop

### Quick Setup Shortcut
Same as above, but use `setup.bat`

## Tips & Best Practices

1. **Always close the app properly** - Press `Ctrl+C` to stop gracefully
2. **Keep Docker running** - Required for database and cache
3. **Update dependencies regularly** - Re-run `setup.bat` after pulling changes
4. **Check logs for errors** - Watch the terminal for error messages
5. **Use .env.example as reference** - Never modify the example file
6. **Back up your .env file** - Contains sensitive API keys

## Security Notes

⚠️ **Important:**
- Never commit `.env` to version control
- Never share your API keys
- Rotate API keys periodically
- Use strong SECRET_KEY in production
- Enable HTTPS in production environments

## Support & Documentation

- **API Docs:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc
- **Development Guide:** See DEVELOPMENT.md
- **Main README:** See README.md
- **GitHub Issues:** https://github.com/pulkitmalik099-ctrl/Enterprise-Hiring-Assistant-System/issues

## Next Steps

1. Run `setup.bat` to prepare your environment
2. Configure your API keys in `.env`
3. Run `run.bat` to start the application
4. Visit http://localhost:8000/api/docs to explore the API
5. Try uploading a resume to test the AI agents

---

Happy hiring! 🚀
