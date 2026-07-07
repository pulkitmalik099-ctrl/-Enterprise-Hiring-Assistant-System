# Enterprise Hiring Assistant System

A multi-agent AI system designed to streamline enterprise recruitment through intelligent resume analysis, job matching, interview preparation, and comprehensive feedback generation.

## 🎯 Overview

This system leverages multiple AI agents to handle various aspects of the hiring pipeline:

- **Resume Analyzer** - Parse and extract key information from candidate resumes
- **Job Matcher** - Match candidates to suitable job positions
- **Interview Prep Coach** - Prepare candidates for upcoming interviews
- **Feedback Generator** - Provide detailed feedback on candidate performance
- **Salary Negotiator** - Assist in salary negotiation discussions
- **Orchestrator** - Coordinate all agents and manage workflow

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 15
- Redis 7
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/pulkitmalik099-ctrl/Enterprise-Hiring-Assistant-System.git
cd Enterprise-Hiring-Assistant-System
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

5. **Start services with Docker:**
```bash
docker-compose up -d
```

6. **Run the application:**
```bash
uvicorn app.main:app --reload
```

7. **Access API documentation:**
Open http://localhost:8000/api/docs in your browser

## 📁 Project Structure

```
Enterprise-Hiring-Assistant-System/
├── app/
│   ├── agents/           # AI agent implementations
│   ├── api/              # API endpoints
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── database/         # Database configuration
│   ├── utils/            # Utility functions
│   ├── services/         # Business logic services
│   ├── config.py         # Configuration settings
│   └── main.py           # FastAPI application entry point
├── tests/
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docker/               # Docker configurations
├── k8s/                  # Kubernetes manifests
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── uploads/              # Temporary file storage
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
└── README.md            # This file
```

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI |
| **Database** | PostgreSQL |
| **Cache** | Redis |
| **LLM** | Anthropic Claude / OpenAI GPT |
| **Agent Framework** | CrewAI |
| **ORM** | SQLAlchemy |
| **Task Queue** | Celery |
| **Container** | Docker |
| **Testing** | Pytest |

## 📚 Development Phases

### Phase 1: Agent Implementation
- [ ] Resume Analyzer Agent
- [ ] Job Matcher Agent
- [ ] Interview Prep Coach
- [ ] Feedback Generator
- [ ] Salary Negotiator
- [ ] Orchestrator Agent

### Phase 2: API Endpoints
- [ ] Candidate upload endpoint
- [ ] Job creation endpoint
- [ ] Workflow execution endpoint
- [ ] Results retrieval endpoint

### Phase 3: Frontend
- [ ] React dashboard
- [ ] Candidate management UI
- [ ] Job listing
- [ ] Results visualization

### Phase 4: Deployment
- [ ] GitHub Actions CI/CD
- [ ] Kubernetes deployment
- [ ] Production monitoring
- [ ] Security hardening

## 🔐 Security Considerations

- Never commit `.env` files with actual API keys
- Use environment variables for sensitive data
- Implement proper authentication and authorization
- Validate and sanitize all user inputs
- Use HTTPS in production
- Regular security audits and updates

## 📝 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🧪 Testing

Run tests with pytest:
```bash
pytest                          # Run all tests
pytest tests/unit               # Run unit tests only
pytest --cov=app               # Run with coverage
```

## 🐳 Docker

Build and run with Docker:
```bash
docker build -t hiring-assistant .
docker run -p 8000:8000 hiring-assistant
```

Or use Docker Compose:
```bash
docker-compose up -d
docker-compose down
```

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub or contact the development team.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please follow the existing code style and submit pull requests with clear descriptions.

---

**Last Updated**: 2026-07-08
