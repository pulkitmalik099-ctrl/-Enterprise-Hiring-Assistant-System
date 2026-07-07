import json
from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent, AgentResponse
from app.config import settings


class InterviewPrepCoach(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Interview Prep Coach",
            description="Prepares candidates for interviews with tailored guidance and practice questions"
        )
        self.api_key = settings.ANTHROPIC_API_KEY

    async def execute(
        self,
        candidate_data: Dict[str, Any],
        job_data: Dict[str, Any],
        interview_type: str = "technical"
    ) -> AgentResponse:
        try:
            if not await self.validate_input(candidate_data=candidate_data, job_data=job_data):
                return AgentResponse(
                    success=False,
                    error="Invalid candidate or job data provided"
                )

            prep_material = await self._generate_prep_material(
                candidate_data,
                job_data,
                interview_type
            )
            processed_material = await self.process_output(prep_material)

            return AgentResponse(
                success=True,
                data=processed_material
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Interview prep generation failed: {str(e)}"
            )

    async def validate_input(self, **kwargs) -> bool:
        candidate_data = kwargs.get("candidate_data", {})
        job_data = kwargs.get("job_data", {})

        return (
            isinstance(candidate_data, dict) and
            isinstance(job_data, dict) and
            "skills" in candidate_data and
            "title" in job_data
        )

    async def _generate_prep_material(
        self,
        candidate_data: Dict[str, Any],
        job_data: Dict[str, Any],
        interview_type: str
    ) -> Dict[str, Any]:
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            candidate_json = json.dumps(candidate_data, indent=2)
            job_json = json.dumps(job_data, indent=2)

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Prepare comprehensive interview preparation material for the candidate applying to this job.

Candidate Profile:
{candidate_json}

Job Description:
{job_json}

Interview Type: {interview_type}

Provide a JSON response with the following structure:
{{
    "interview_type": "{interview_type}",
    "key_topics": ["topic1", "topic2"],
    "practice_questions": [
        {{
            "question": "Question text",
            "expected_areas": "What to cover",
            "sample_answer": "Example answer",
            "follow_ups": ["follow-up1", "follow-up2"]
        }}
    ],
    "strengths_to_highlight": ["strength1", "strength2"],
    "potential_concerns": [
        {{
            "concern": "Potential gap",
            "talking_point": "How to address it"
        }}
    ],
    "company_research": ["fact1", "fact2"],
    "technical_preparation": {{"focus_areas": ["area1", "area2"]}},
    "tips_and_tricks": ["tip1", "tip2"]
}}"""
                    }
                ]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                prep_material = json.loads(json_str)
                return prep_material
            else:
                return {}

        except Exception as e:
            raise Exception(f"Interview prep generation error: {str(e)}")

    async def process_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["material_count"] = {
            "practice_questions": len(data.get("practice_questions", [])),
            "key_topics": len(data.get("key_topics", [])),
            "strengths": len(data.get("strengths_to_highlight", [])),
            "concerns": len(data.get("potential_concerns", []))
        }
        return data
