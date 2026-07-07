from typing import Dict, Any, List, Optional
from app.agents.base_agent import AgentResponse
from app.agents.resume_analyzer import ResumeAnalyzerAgent
from app.agents.job_matcher import JobMatcherAgent
from app.agents.interview_prep import InterviewPrepCoach
from app.agents.feedback_generator import FeedbackGenerator
from app.agents.salary_negotiator import SalaryNegotiator


class OrchestratorAgent:
    def __init__(self):
        self.resume_analyzer = ResumeAnalyzerAgent()
        self.job_matcher = JobMatcherAgent()
        self.interview_prep = InterviewPrepCoach()
        self.feedback_generator = FeedbackGenerator()
        self.salary_negotiator = SalaryNegotiator()

    async def execute_full_pipeline(
        self,
        resume_text: str,
        candidate_email: str,
        available_jobs: List[Dict[str, Any]],
        interview_type: str = "technical"
    ) -> Dict[str, Any]:
        """Execute the complete hiring pipeline for a candidate."""
        results = {
            "candidate_email": candidate_email,
            "pipeline_stages": {}
        }

        # Stage 1: Analyze Resume
        resume_analysis = await self.resume_analyzer.execute(
            resume_text=resume_text,
            candidate_email=candidate_email
        )
        results["pipeline_stages"]["resume_analysis"] = resume_analysis.dict()

        if not resume_analysis.success:
            return results

        candidate_data = resume_analysis.data

        # Stage 2: Match to Jobs
        job_match_result = await self.job_matcher.execute(
            candidate_data=candidate_data,
            available_jobs=available_jobs
        )
        results["pipeline_stages"]["job_matches"] = job_match_result.dict()

        if job_match_result.success and job_match_result.data["matches"]:
            top_match = job_match_result.data["matches"][0]

            # Stage 3: Generate Interview Prep
            interview_prep_result = await self.interview_prep.execute(
                candidate_data=candidate_data,
                job_data=top_match,
                interview_type=interview_type
            )
            results["pipeline_stages"]["interview_prep"] = interview_prep_result.dict()

        results["summary"] = self._generate_summary(results)
        return results

    async def execute_interview_feedback_pipeline(
        self,
        candidate_data: Dict[str, Any],
        interview_performance: Dict[str, Any],
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute feedback and salary negotiation after interview."""
        results = {
            "candidate_email": candidate_data.get("email"),
            "pipeline_stages": {}
        }

        # Stage 1: Generate Feedback
        feedback_result = await self.feedback_generator.execute(
            candidate_data=candidate_data,
            interview_performance=interview_performance,
            job_data=job_data
        )
        results["pipeline_stages"]["interview_feedback"] = feedback_result.dict()

        # Stage 2: Salary Negotiation (if recommended)
        if feedback_result.success and feedback_result.data.get("recommendation") == "HIRE":
            salary_result = await self.salary_negotiator.execute(
                candidate_data=candidate_data,
                job_data=job_data
            )
            results["pipeline_stages"]["salary_analysis"] = salary_result.dict()

        results["summary"] = self._generate_summary(results)
        return results

    async def execute_specific_agent(
        self,
        agent_name: str,
        **kwargs
    ) -> AgentResponse:
        """Execute a specific agent with provided parameters."""
        agent_map = {
            "resume_analyzer": self.resume_analyzer.execute,
            "job_matcher": self.job_matcher.execute,
            "interview_prep": self.interview_prep.execute,
            "feedback_generator": self.feedback_generator.execute,
            "salary_negotiator": self.salary_negotiator.execute
        }

        if agent_name not in agent_map:
            return AgentResponse(
                success=False,
                error=f"Unknown agent: {agent_name}"
            )

        try:
            result = await agent_map[agent_name](**kwargs)
            return result
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Agent execution failed: {str(e)}"
            )

    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the pipeline results."""
        summary = {
            "total_stages": len(results.get("pipeline_stages", {})),
            "completed_stages": sum(
                1 for stage in results.get("pipeline_stages", {}).values()
                if stage.get("success", False)
            ),
            "status": "completed" if all(
                stage.get("success", False)
                for stage in results.get("pipeline_stages", {}).values()
            ) else "partial",
            "key_findings": self._extract_key_findings(results)
        }
        return summary

    def _extract_key_findings(self, results: Dict[str, Any]) -> List[str]:
        """Extract key findings from pipeline results."""
        findings = []

        stages = results.get("pipeline_stages", {})

        if "resume_analysis" in stages:
            analysis = stages["resume_analysis"].get("data", {})
            if analysis:
                completeness = analysis.get("quality_indicators", {}).get("completeness", 0)
                findings.append(f"Resume completeness: {completeness:.1f}%")

        if "job_matches" in stages:
            matches = stages["job_matches"].get("data", {}).get("matches", [])
            if matches:
                top_score = matches[0].get("match_score", 0)
                findings.append(f"Best job match score: {top_score}/100")

        if "interview_feedback" in stages:
            feedback = stages["interview_feedback"].get("data", {})
            if feedback:
                rating = feedback.get("rating", "N/A")
                finding = feedback.get("recommendation", "UNKNOWN")
                findings.append(f"Interview recommendation: {finding} (Rating: {rating})")

        return findings
