import json
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent, AgentResponse
from app.config import settings


class JobMatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Job Matcher",
            description="Matches candidates to suitable job positions based on skills and experience"
        )
        self.api_key = settings.ANTHROPIC_API_KEY

    async def execute(
        self,
        candidate_data: Dict[str, Any],
        available_jobs: List[Dict[str, Any]]
    ) -> AgentResponse:
        try:
            if not await self.validate_input(candidate_data=candidate_data, available_jobs=available_jobs):
                return AgentResponse(
                    success=False,
                    error="Invalid candidate or job data provided"
                )

            matches = await self._match_jobs(candidate_data, available_jobs)
            processed_matches = await self.process_output({"matches": matches})

            return AgentResponse(
                success=True,
                data=processed_matches
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Job matching failed: {str(e)}"
            )

    async def validate_input(self, **kwargs) -> bool:
        candidate_data = kwargs.get("candidate_data", {})
        available_jobs = kwargs.get("available_jobs", [])

        return (
            isinstance(candidate_data, dict) and
            "skills" in candidate_data and
            isinstance(available_jobs, list) and
            len(available_jobs) > 0
        )

    async def _match_jobs(
        self,
        candidate_data: Dict[str, Any],
        available_jobs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            jobs_json = json.dumps(available_jobs, indent=2)
            candidate_json = json.dumps(candidate_data, indent=2)

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze the following candidate profile and match them to suitable job positions.

Candidate Profile:
{candidate_json}

Available Jobs:
{jobs_json}

For each job, provide a match score (0-100) and explain why the candidate is or isn't a good fit.
Return a JSON array with the following structure:
[
    {{
        "job_id": "Job ID",
        "job_title": "Job Title",
        "match_score": 85,
        "match_reasons": ["reason1", "reason2"],
        "skill_gaps": ["skill1", "skill2"],
        "experience_alignment": "How well experience aligns",
        "recommendation": "STRONG_MATCH" | "GOOD_MATCH" | "MODERATE_MATCH" | "POOR_MATCH"
    }}
]

Sort by match_score in descending order."""
                    }
                ]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                matches = json.loads(json_str)
                return matches
            else:
                return []

        except Exception as e:
            raise Exception(f"Job matching error: {str(e)}")

    async def process_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        matches = data.get("matches", [])
        data["summary"] = {
            "total_matches": len(matches),
            "strong_matches": len([m for m in matches if m.get("recommendation") == "STRONG_MATCH"]),
            "good_matches": len([m for m in matches if m.get("recommendation") == "GOOD_MATCH"]),
            "top_match": matches[0] if matches else None
        }
        return data
