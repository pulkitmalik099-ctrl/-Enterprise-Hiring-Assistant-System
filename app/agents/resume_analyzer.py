import json
from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent, AgentResponse
from app.config import settings


class ResumeAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Resume Analyzer",
            description="Analyzes candidate resumes and extracts key information"
        )
        self.api_key = settings.ANTHROPIC_API_KEY

    async def execute(self, resume_text: str, candidate_email: Optional[str] = None) -> AgentResponse:
        try:
            if not await self.validate_input(resume_text=resume_text):
                return AgentResponse(
                    success=False,
                    error="Invalid resume text provided"
                )

            parsed_data = await self._parse_resume(resume_text)
            processed_data = await self.process_output(parsed_data)

            return AgentResponse(
                success=True,
                data=processed_data,
                metadata={"candidate_email": candidate_email}
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Resume analysis failed: {str(e)}"
            )

    async def validate_input(self, **kwargs) -> bool:
        resume_text = kwargs.get("resume_text", "")
        return len(resume_text.strip()) > 50

    async def _parse_resume(self, resume_text: str) -> Dict[str, Any]:
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze the following resume and extract key information in JSON format.

Resume:
{resume_text}

Please provide a JSON response with the following structure:
{{
    "name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "location": "Location/City",
    "summary": "Professional summary",
    "skills": ["skill1", "skill2", ...],
    "experience": [
        {{
            "title": "Job title",
            "company": "Company name",
            "duration": "Duration",
            "description": "Job description"
        }}
    ],
    "education": [
        {{
            "degree": "Degree",
            "institution": "Institution name",
            "field": "Field of study"
        }}
    ],
    "certifications": ["cert1", "cert2"],
    "languages": ["language1", "language2"],
    "key_achievements": ["achievement1", "achievement2"]
}}

If any field is not found, use null. Return only valid JSON."""
                    }
                ]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                parsed_data = json.loads(json_str)
                return parsed_data
            else:
                return {"error": "Could not parse resume"}

        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    async def process_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["analysis_type"] = "resume_parsing"
        data["quality_indicators"] = {
            "has_skills": bool(data.get("skills")),
            "has_experience": bool(data.get("experience")),
            "has_education": bool(data.get("education")),
            "completeness": self._calculate_completeness(data)
        }
        return data

    def _calculate_completeness(self, data: Dict[str, Any]) -> float:
        required_fields = ["name", "email", "skills", "experience", "education"]
        present = sum(1 for field in required_fields if data.get(field))
        return (present / len(required_fields)) * 100
