import json
from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent, AgentResponse
from app.config import settings


class SalaryNegotiator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Salary Negotiator",
            description="Assists in salary negotiation and compensation analysis"
        )
        self.api_key = settings.ANTHROPIC_API_KEY

    async def execute(
        self,
        candidate_data: Dict[str, Any],
        job_data: Dict[str, Any],
        market_data: Optional[Dict[str, Any]] = None,
        offer_salary: Optional[float] = None
    ) -> AgentResponse:
        try:
            if not await self.validate_input(candidate_data=candidate_data, job_data=job_data):
                return AgentResponse(
                    success=False,
                    error="Invalid candidate or job data provided"
                )

            analysis = await self._analyze_compensation(
                candidate_data,
                job_data,
                market_data,
                offer_salary
            )
            processed_analysis = await self.process_output(analysis)

            return AgentResponse(
                success=True,
                data=processed_analysis
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Salary analysis failed: {str(e)}"
            )

    async def validate_input(self, **kwargs) -> bool:
        candidate_data = kwargs.get("candidate_data", {})
        job_data = kwargs.get("job_data", {})

        return (
            isinstance(candidate_data, dict) and
            isinstance(job_data, dict) and
            "experience" in candidate_data
        )

    async def _analyze_compensation(
        self,
        candidate_data: Dict[str, Any],
        job_data: Dict[str, Any],
        market_data: Optional[Dict[str, Any]] = None,
        offer_salary: Optional[float] = None
    ) -> Dict[str, Any]:
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            candidate_json = json.dumps(candidate_data, indent=2)
            job_json = json.dumps(job_data, indent=2)
            market_json = json.dumps(market_data or {}, indent=2)
            offer_str = str(offer_salary) if offer_salary else "Not provided"

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze the salary and compensation for this candidate and position.

Candidate Profile:
{candidate_json}

Job Description:
{job_json}

Market Data:
{market_json}

Current Offer: ${offer_str}

Provide a JSON response with the following structure:
{{
    "candidate_profile_value": {{
        "experience_level": "Junior" | "Mid" | "Senior" | "Lead",
        "skill_level": "Average" | "Good" | "Excellent",
        "estimated_market_value": 150000,
        "value_assessment": "Description of value"
    }},
    "market_analysis": {{
        "role_market_rate": 155000,
        "industry_benchmark": 160000,
        "location_adjustment": 1.1,
        "competitive_range": "150000-180000"
    }},
    "compensation_recommendation": {{
        "base_salary": 160000,
        "bonus_percentage": 15,
        "equity": "Optional details",
        "benefits": ["benefit1", "benefit2"],
        "total_compensation": 184000
    }},
    "negotiation_strategy": [
        {{
            "point": "Negotiation talking point",
            "rationale": "Why this matters",
            "expected_response": "How employer might respond"
        }}
    ],
    "acceptance_threshold": {{
        "minimum": 150000,
        "ideal": 165000,
        "maximum": 180000
    }},
    "negotiation_tips": ["tip1", "tip2"]
}}"""
                    }
                ]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                analysis = json.loads(json_str)
                return analysis
            else:
                return {}

        except Exception as e:
            raise Exception(f"Salary analysis error: {str(e)}")

    async def process_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        base_salary = data.get("compensation_recommendation", {}).get("base_salary", 0)
        offer_salary = data.get("current_offer", 0)

        if offer_salary and base_salary:
            difference = ((base_salary - offer_salary) / offer_salary) * 100
            data["negotiation_opportunity"] = {
                "offer_salary": offer_salary,
                "recommended_salary": base_salary,
                "difference_percentage": round(difference, 2),
                "gap_amount": round(base_salary - offer_salary, 2)
            }

        return data
