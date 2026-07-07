import React, { useState } from 'react';
import { Play, Loader } from 'lucide-react';
import { workflowsAPI } from '../services/api';
import { useLoading, useError } from '../utils/hooks';
import './Workflows.css';

const Workflows = () => {
  const [activeTab, setActiveTab] = useState('full-pipeline');
  const [resumeText, setResumeText] = useState('');
  const [candidateEmail, setCandidateEmail] = useState('');
  const [results, setResults] = useState(null);
  const { loading, setLoading } = useLoading();
  const { error, setError, clearError } = useError();

  const handleExecuteFullPipeline = async (e) => {
    e.preventDefault();

    if (!resumeText.trim() || !candidateEmail.trim()) {
      setError('Please fill in all fields');
      return;
    }

    try {
      setLoading(true);
      clearError();
      const response = await workflowsAPI.fullPipeline(
        resumeText,
        candidateEmail,
        null,
        'technical'
      );
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to execute workflow');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const ResultsPanel = ({ data }) => {
    if (!data) return null;

    const resumeAnalysis = data.pipeline_stages?.resume_analysis;
    const jobMatches = data.pipeline_stages?.job_matches;
    const interviewPrep = data.pipeline_stages?.interview_prep;

    return (
      <div className="results-panel">
        <h3>Pipeline Results</h3>

        {resumeAnalysis?.success && (
          <div className="result-section">
            <h4>📄 Resume Analysis</h4>
            {resumeAnalysis.data?.quality_indicators && (
              <div className="indicators">
                <p><strong>Completeness:</strong> {resumeAnalysis.data.quality_indicators.completeness.toFixed(1)}%</p>
                <p><strong>Has Skills:</strong> {resumeAnalysis.data.quality_indicators.has_skills ? '✓' : '✗'}</p>
                <p><strong>Has Experience:</strong> {resumeAnalysis.data.quality_indicators.has_experience ? '✓' : '✗'}</p>
                <p><strong>Has Education:</strong> {resumeAnalysis.data.quality_indicators.has_education ? '✓' : '✗'}</p>
              </div>
            )}
          </div>
        )}

        {jobMatches?.success && jobMatches.data?.matches?.length > 0 && (
          <div className="result-section">
            <h4>🎯 Job Matches</h4>
            <p><strong>Total Matches:</strong> {jobMatches.data.summary?.total_matches}</p>
            <p><strong>Strong Matches:</strong> {jobMatches.data.summary?.strong_matches}</p>
            <p><strong>Good Matches:</strong> {jobMatches.data.summary?.good_matches}</p>
          </div>
        )}

        {interviewPrep?.success && (
          <div className="result-section">
            <h4>🎓 Interview Prep</h4>
            {interviewPrep.data?.material_count && (
              <div className="indicators">
                <p><strong>Practice Questions:</strong> {interviewPrep.data.material_count.practice_questions}</p>
                <p><strong>Key Topics:</strong> {interviewPrep.data.material_count.key_topics}</p>
                <p><strong>Strengths to Highlight:</strong> {interviewPrep.data.material_count.strengths}</p>
              </div>
            )}
          </div>
        )}

        {data.summary && (
          <div className="result-section summary">
            <h4>📊 Summary</h4>
            <p><strong>Completed Stages:</strong> {data.summary.completed_stages}/{data.summary.total_stages}</p>
            <p><strong>Status:</strong> {data.summary.status}</p>
            {data.summary.key_findings?.length > 0 && (
              <ul>
                {data.summary.key_findings.map((finding, idx) => (
                  <li key={idx}>{finding}</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="workflows-page">
      <h1>AI Workflows</h1>
      <p className="subtitle">Execute intelligent hiring workflows powered by AI agents</p>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={clearError} style={{ marginLeft: '1rem' }}>×</button>
        </div>
      )}

      <div className="workflow-container">
        {/* Tab Navigation */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'full-pipeline' ? 'active' : ''}`}
            onClick={() => setActiveTab('full-pipeline')}
          >
            Full Pipeline
          </button>
          <button
            className={`tab ${activeTab === 'info' ? 'active' : ''}`}
            onClick={() => setActiveTab('info')}
          >
            Agent Info
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'full-pipeline' && (
            <div className="workflow-section card">
              <h2>Complete Hiring Pipeline</h2>
              <p>Execute all AI agents in sequence for comprehensive candidate analysis:</p>
              <ol className="agent-flow">
                <li><strong>Resume Analyzer</strong> - Parse and extract candidate information</li>
                <li><strong>Job Matcher</strong> - Match candidate to available positions</li>
                <li><strong>Interview Prep Coach</strong> - Generate interview preparation materials</li>
              </ol>

              <form onSubmit={handleExecuteFullPipeline} className="workflow-form">
                <div className="form-group">
                  <label>Candidate Email *</label>
                  <input
                    type="email"
                    value={candidateEmail}
                    onChange={(e) => setCandidateEmail(e.target.value)}
                    placeholder="candidate@example.com"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Resume Text *</label>
                  <textarea
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    placeholder="Paste resume content here..."
                    rows="10"
                    required
                  ></textarea>
                  <small>
                    Paste your resume text directly. Include work experience, education, skills, etc.
                  </small>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader size={20} className="spinning" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Play size={20} />
                      Execute Workflow
                    </>
                  )}
                </button>
              </form>

              {results && <ResultsPanel data={results} />}
            </div>
          )}

          {activeTab === 'info' && (
            <div className="agents-info card">
              <h2>AI Agents Overview</h2>

              <div className="agent-info-grid">
                <div className="agent-card">
                  <h3>📄 Resume Analyzer</h3>
                  <p>Parses resumes and extracts:</p>
                  <ul>
                    <li>Personal information</li>
                    <li>Work experience</li>
                    <li>Educational background</li>
                    <li>Technical skills</li>
                    <li>Certifications</li>
                  </ul>
                </div>

                <div className="agent-card">
                  <h3>🎯 Job Matcher</h3>
                  <p>Matches candidates to positions based on:</p>
                  <ul>
                    <li>Skill alignment</li>
                    <li>Experience level</li>
                    <li>Salary expectations</li>
                    <li>Location preferences</li>
                    <li>Career goals</li>
                  </ul>
                </div>

                <div className="agent-card">
                  <h3>🎓 Interview Prep Coach</h3>
                  <p>Prepares candidates with:</p>
                  <ul>
                    <li>Practice questions</li>
                    <li>Company research</li>
                    <li>Technical preparation</li>
                    <li>Behavioral tips</li>
                    <li>Strengths to highlight</li>
                  </ul>
                </div>

                <div className="agent-card">
                  <h3>📝 Feedback Generator</h3>
                  <p>Creates comprehensive feedback on:</p>
                  <ul>
                    <li>Interview performance</li>
                    <li>Technical competency</li>
                    <li>Cultural fit assessment</li>
                    <li>Growth potential</li>
                    <li>Recommendation</li>
                  </ul>
                </div>

                <div className="agent-card">
                  <h3>💰 Salary Negotiator</h3>
                  <p>Analyzes compensation based on:</p>
                  <ul>
                    <li>Market rates</li>
                    <li>Candidate experience</li>
                    <li>Industry benchmarks</li>
                    <li>Location adjustments</li>
                    <li>Negotiation strategy</li>
                  </ul>
                </div>

                <div className="agent-card">
                  <h3>🎭 Orchestrator</h3>
                  <p>Coordinates all agents for:</p>
                  <ul>
                    <li>Sequential execution</li>
                    <li>Data flow management</li>
                    <li>Result compilation</li>
                    <li>Error handling</li>
                    <li>Pipeline optimization</li>
                  </ul>
                </div>
              </div>

              <div className="workflow-benefits">
                <h3>Benefits of Using AI Workflows</h3>
                <ul>
                  <li>⚡ <strong>Speed:</strong> Analyze candidates in minutes instead of hours</li>
                  <li>📊 <strong>Consistency:</strong> Standardized evaluation across all candidates</li>
                  <li>🎯 <strong>Accuracy:</strong> AI-powered insights reduce human bias</li>
                  <li>💡 <strong>Insights:</strong> Deep analysis reveals hidden candidate potential</li>
                  <li>📈 <strong>Scalability:</strong> Process hundreds of candidates efficiently</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Workflows;
