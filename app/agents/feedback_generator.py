import json
from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent, AgentResponse
from app.config import settings


class FeedbackGenerator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Feedback Generator",
            description="Generates comprehensive feedback on candidate performance and interview results"
        )
        self.api_key = settings.ANTHROPIC_API_KEY

    async def execute(
        self,
        candidate_data: Dict[str, Any],
        interview_performance: Dict[str, Any],
        job_data: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        try:
            if not await self.validate_input(
                candidate_data=candidate_data,
                interview_performance=interview_performance
            ):
                return AgentResponse(
                    success=False,
                    error="Invalid candidate or performance data provided"
                )

            feedback = await self._generate_feedback(
                candidate_data,
                interview_performance,
                job_data
            )
            processed_feedback = await self.process_output(feedback)

            return AgentResponse(
                success=True,
                data=processed_feedback
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Feedback generation failed: {str(e)}"
            )

    async def validate_input(self, **kwargs) -> bool:
        candidate_data = kwargs.get("candidate_data", {})
        interview_performance = kwargs.get("interview_performance", {})

        return (
            isinstance(candidate_data, dict) and
            isinstance(interview_performance, dict) and
            len(interview_performance) > 0
        )

    async def _generate_feedback(
        self,
        candidate_data: Dict[str, Any],
        interview_performance: Dict[str, Any],
        job_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            candidate_json = json.dumps(candidate_data, indent=2)
            performance_json = json.dumps(interview_performance, indent=2)
            job_json = json.dumps(job_data, indent=2) if job_data else "N/A"

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Generate comprehensive feedback for this candidate based on their interview performance.

Candidate Profile:
{candidate_json}

Interview Performance:
{performance_json}

Job Requirements:
{job_json}

Provide a JSON response with the following structure:
{{
    "overall_assessment": "Summary of overall performance",
    "rating": 7.5,
    "strengths": [
        {{
            "area": "Technical skills",
            "observation": "Specific observation",
            "impact": "Why this matters"
        }}
    ],
    "areas_for_improvement": [
        {{
            "area": "Area needing improvement",
            "observation": "Specific observation",
            "suggestion": "How to improve",
            "priority": "HIGH" | "MEDIUM" | "LOW"
        }}
    ],
    "job_fit_analysis": {{
        "technical_fit": 8,
        "cultural_fit": 7,
        "growth_potential": 8,
        "overall_fit": 7.5
    }},
    "recommendation": "HIRE" | "MAYBE" | "REJECT",
    "next_steps": ["step1", "step2"],
    "key_questions_for_next_round": ["question1", "question2"],
    "final_comments": "Additional remarks"
}}"""
                    }
                ]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                feedback = json.loads(json_str)
                return feedback
            else:
                return {}

        except Exception as e:
            raise Exception(f"Feedback generation error: {str(e)}")

    async def process_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["feedback_summary"] = {
            "strengths_count": len(data.get("strengths", [])),
            "improvements_count": len(data.get("areas_for_improvement", [])),
            "rating": data.get("rating", 0),
            "recommendation": data.get("recommendation", "UNKNOWN")
        }
        return data
