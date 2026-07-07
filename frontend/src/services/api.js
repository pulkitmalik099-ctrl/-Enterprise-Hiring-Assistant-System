import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Candidates API
export const candidatesAPI = {
  list: (skip = 0, limit = 10) =>
    api.get('/candidates/', { params: { skip, limit } }),

  get: (id) =>
    api.get(`/candidates/${id}`),

  create: (data) =>
    api.post('/candidates/analyze', data),

  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/candidates/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  update: (id, data) =>
    api.put(`/candidates/${id}`, data),

  delete: (id) =>
    api.delete(`/candidates/${id}`),
};

// Jobs API
export const jobsAPI = {
  list: (status = 'open', skip = 0, limit = 10) =>
    api.get('/jobs/', { params: { status, skip, limit } }),

  get: (id) =>
    api.get(`/jobs/${id}`),

  create: (data) =>
    api.post('/jobs/', data),

  update: (id, data) =>
    api.put(`/jobs/${id}`, data),

  delete: (id) =>
    api.delete(`/jobs/${id}`),

  matchCandidates: (jobId, candidateIds) =>
    api.post(`/jobs/${jobId}/match-candidates`, { candidate_ids: candidateIds }),
};

// Workflows API
export const workflowsAPI = {
  analyzeResume: (resumeText, candidateEmail, availableJobs = null) =>
    api.post('/workflows/analyze-resume', {
      resume_text: resumeText,
      candidate_email: candidateEmail,
      available_jobs: availableJobs,
      interview_type: 'technical',
    }),

  interviewFeedback: (candidateData, interviewPerformance, jobData, offerSalary = null) =>
    api.post('/workflows/interview-feedback', {
      candidate_data: candidateData,
      interview_performance: interviewPerformance,
      job_data: jobData,
      offer_salary: offerSalary,
    }),

  fullPipeline: (resumeText, candidateEmail, availableJobIds = null, interviewType = 'technical') =>
    api.post('/workflows/full-pipeline', {
      resume_text: resumeText,
      candidate_email: candidateEmail,
      available_job_ids: availableJobIds,
      interview_type: interviewType,
    }),

  executeAgent: (agentName, params) =>
    api.post(`/workflows/agent/${agentName}`, params),
};

// Health check
export const health = () =>
  api.get('/');

export default api;
