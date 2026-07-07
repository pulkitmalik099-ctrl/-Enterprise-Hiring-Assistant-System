# Development Guide

## Overview

This document provides detailed information about the Enterprise Hiring Assistant System architecture, agents, and API endpoints.

## Project Structure

```
Enterprise-Hiring-Assistant-System/
├── app/
│   ├── agents/              # Multi-agent AI system
│   │   ├── base_agent.py    # Abstract base agent class
│   │   ├── resume_analyzer.py
│   │   ├── job_matcher.py
│   │   ├── interview_prep.py
│   │   ├── feedback_generator.py
│   │   ├── salary_negotiator.py
│   │   └── orchestrator.py  # Agent coordinator
│   ├── api/                 # REST API endpoints
│   │   ├── candidates.py
│   │   ├── jobs.py
│   │   └── workflows.py
│   ├── models/              # SQLAlchemy models
│   │   ├── candidate.py
│   │   └── job.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── candidate.py
│   │   └── job.py
│   ├── database/
│   │   └── db.py            # Database configuration
│   ├── config.py            # Application settings
│   └── main.py              # FastAPI app entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py          # Pytest configuration
├── .github/workflows/       # CI/CD workflows
│   ├── test.yml
│   ├── docker.yml
│   └── security.yml
└── docker-compose.yml       # Local development setup
```

## AI Agents

### 1. Resume Analyzer Agent
**Purpose:** Parse and extract key information from candidate resumes

**Input:**
- `resume_text`: Full text of the resume
- `candidate_email`: Email of the candidate (optional)

**Output:**
```json
{
  "name": "Full name",
  "email": "Email",
  "phone": "Phone number",
  "location": "Location",
  "summary": "Professional summary",
  "skills": ["skill1", "skill2"],
  "experience": [{"title", "company", "duration", "description"}],
  "education": [{"degree", "institution", "field"}],
  "certifications": ["cert1"],
  "languages": ["lang1"],
  "key_achievements": ["achievement1"],
  "quality_indicators": {
    "has_skills": true,
    "has_experience": true,
    "has_education": true,
    "completeness": 85.5
  }
}
```

**API Endpoint:**
```bash
POST /api/workflows/analyze-resume
```

### 2. Job Matcher Agent
**Purpose:** Match candidates to suitable job positions based on skills and experience

**Input:**
- `candidate_data`: Parsed candidate information
- `available_jobs`: List of job positions to match against

**Output:**
```json
{
  "matches": [
    {
      "job_id": "job-uuid",
      "job_title": "Senior Engineer",
      "match_score": 85,
      "match_reasons": ["reason1", "reason2"],
      "skill_gaps": ["skill1"],
      "experience_alignment": "description",
      "recommendation": "STRONG_MATCH"
    }
  ],
  "summary": {
    "total_matches": 1,
    "strong_matches": 1,
    "good_matches": 0,
    "top_match": {...}
  }
}
```

### 3. Interview Prep Coach
**Purpose:** Prepare candidates for interviews with tailored guidance

**Input:**
- `candidate_data`: Parsed candidate information
- `job_data`: Target job position details
- `interview_type`: "technical", "behavioral", or "cultural" (default: "technical")

**Output:**
```json
{
  "interview_type": "technical",
  "key_topics": ["topic1", "topic2"],
  "practice_questions": [
    {
      "question": "Question text",
      "expected_areas": "What to cover",
      "sample_answer": "Example",
      "follow_ups": ["follow-up1"]
    }
  ],
  "strengths_to_highlight": ["strength1"],
  "potential_concerns": [{"concern", "talking_point"}],
  "company_research": ["fact1"],
  "technical_preparation": {"focus_areas": ["area1"]},
  "tips_and_tricks": ["tip1"]
}
```

### 4. Feedback Generator
**Purpose:** Generate comprehensive feedback on candidate interview performance

**Input:**
- `candidate_data`: Candidate information
- `interview_performance`: Performance metrics and notes
- `job_data`: Job position details (optional)

**Output:**
```json
{
  "overall_assessment": "Summary",
  "rating": 7.5,
  "strengths": [{"area", "observation", "impact"}],
  "areas_for_improvement": [{"area", "observation", "suggestion", "priority"}],
  "job_fit_analysis": {
    "technical_fit": 8,
    "cultural_fit": 7,
    "growth_potential": 8,
    "overall_fit": 7.5
  },
  "recommendation": "HIRE",
  "next_steps": ["step1"],
  "key_questions_for_next_round": ["question1"],
  "final_comments": "Additional remarks"
}
```

### 5. Salary Negotiator
**Purpose:** Assist in salary negotiation and compensation analysis

**Input:**
- `candidate_data`: Candidate information with experience
- `job_data`: Job position details with salary range
- `market_data`: Market research data (optional)
- `offer_salary`: Current salary offer (optional)

**Output:**
```json
{
  "candidate_profile_value": {
    "experience_level": "Senior",
    "skill_level": "Excellent",
    "estimated_market_value": 150000,
    "value_assessment": "Description"
  },
  "market_analysis": {
    "role_market_rate": 155000,
    "industry_benchmark": 160000,
    "location_adjustment": 1.1,
    "competitive_range": "150000-180000"
  },
  "compensation_recommendation": {
    "base_salary": 160000,
    "bonus_percentage": 15,
    "equity": "Details",
    "benefits": ["benefit1"],
    "total_compensation": 184000
  },
  "negotiation_strategy": [{"point", "rationale", "expected_response"}],
  "acceptance_threshold": {
    "minimum": 150000,
    "ideal": 165000,
    "maximum": 180000
  },
  "negotiation_tips": ["tip1"]
}
```

### 6. Orchestrator Agent
**Purpose:** Coordinate multiple agents and manage workflows

**Methods:**
- `execute_full_pipeline()`: Run complete hiring workflow
- `execute_interview_feedback_pipeline()`: Run interview feedback workflow
- `execute_specific_agent()`: Run individual agent with custom params

## API Endpoints

### Candidates
```
POST   /api/candidates/upload           Upload and analyze resume
POST   /api/candidates/analyze          Analyze candidate data
GET    /api/candidates/{id}             Get candidate details
GET    /api/candidates/                 List all candidates
PUT    /api/candidates/{id}             Update candidate
DELETE /api/candidates/{id}             Delete candidate
```

### Jobs
```
POST   /api/jobs/                       Create job requisition
GET    /api/jobs/{id}                   Get job details
GET    /api/jobs/                       List jobs
PUT    /api/jobs/{id}                   Update job
DELETE /api/jobs/{id}                   Delete job
POST   /api/jobs/{id}/match-candidates  Match candidates to job
```

### Workflows
```
POST /api/workflows/analyze-resume      Analyze resume with optional job matching
POST /api/workflows/interview-feedback  Generate post-interview feedback
POST /api/workflows/full-pipeline       Execute complete hiring pipeline
POST /api/workflows/agent/{agent_name}  Execute specific agent
```

## Environment Variables

Required in `.env`:
```
# Application
APP_NAME=Enterprise Hiring Assistant
DEBUG=False
ENVIRONMENT=production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/hiring_db

# LLM APIs
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here (optional)

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
```

## Running Locally

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL (via Docker)
- Redis (via Docker)

### Steps
1. Create `.env` from `.env.example`
2. Start services: `docker-compose up -d`
3. Install dependencies: `pip install -r requirements.txt`
4. Run app: `uvicorn app.main:app --reload`
5. Visit http://localhost:8000/api/docs

### Testing
```bash
pytest                          # Run all tests
pytest tests/unit -v            # Run unit tests with verbose output
pytest --cov=app               # Run with coverage report
```

## CI/CD Workflows

### test.yml
- Runs on push/PR to main/develop
- Tests with pytest
- Coverage reporting to Codecov
- Linting checks (flake8, black)

### docker.yml
- Builds Docker image on pushes
- Pushes to GitHub Container Registry
- Supports tagged releases

### security.yml
- Weekly security scanning
- Bandit for Python security
- Trivy for dependency scanning
- SARIF reporting

## Development Workflow

1. Create feature branch from `main`
2. Make changes and commit
3. Push branch and create PR
4. CI/CD checks run automatically
5. Once approved and passed, merge to `main`
6. Deployment happens automatically on tag

## Agent Development

To add a new agent:

1. Create class extending `BaseAgent`
2. Implement `execute()` method
3. Add validation in `validate_input()`
4. Add post-processing in `process_output()`
5. Register in `OrchestratorAgent`
6. Create API endpoint in appropriate router
7. Add tests in `tests/unit/`

Example:
```python
class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__("Agent Name", "Description")

    async def execute(self, **kwargs) -> AgentResponse:
        try:
            if not await self.validate_input(**kwargs):
                return AgentResponse(success=False, error="Invalid input")
            
            result = await self._process(**kwargs)
            processed = await self.process_output(result)
            
            return AgentResponse(success=True, data=processed)
        except Exception as e:
            return AgentResponse(success=False, error=str(e))

    async def validate_input(self, **kwargs) -> bool:
        # Validation logic
        return True

    async def _process(self, **kwargs):
        # Implementation
        pass
```

## Performance Considerations

1. **Caching:** Implement Redis caching for expensive LLM calls
2. **Rate Limiting:** Add rate limiting on API endpoints
3. **Background Jobs:** Use Celery for long-running tasks
4. **Database:** Add indexes on frequently queried columns
5. **API Response:** Implement pagination for list endpoints

## Security Checklist

- [ ] Validate all user inputs
- [ ] Sanitize database queries (using SQLAlchemy)
- [ ] Use HTTPS in production
- [ ] Store secrets in environment variables
- [ ] Implement authentication/authorization
- [ ] Add rate limiting
- [ ] Enable CORS selectively
- [ ] Use security headers
- [ ] Regular dependency updates
- [ ] Audit logging

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL container
docker ps
docker logs hiring_db

# Reset database
docker-compose down -v
docker-compose up -d
```

### API Port Already in Use
```bash
# Use different port
uvicorn app.main:app --port 8001
```

### Agent API Key Issues
```bash
# Verify .env variables
echo $ANTHROPIC_API_KEY
# Should be your actual API key, not "test-key"
```

---

Last Updated: 2026-07-08
