import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Eye, Edit2 } from 'lucide-react';
import { jobsAPI } from '../services/api';
import { useLoading, useError } from '../utils/hooks';
import './Jobs.css';

const Jobs = () => {
  const [jobs, setJobs] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const { loading, setLoading } = useLoading();
  const { error, setError, clearError } = useError();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    required_skills: '',
    nice_to_have_skills: '',
    required_experience_years: '',
    location: '',
    salary_range_min: '',
    salary_range_max: '',
    department: '',
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const response = await jobsAPI.list('open', 0, 50);
      setJobs(response.data || []);
      clearError();
    } catch (err) {
      setError('Failed to load jobs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      ...formData,
      required_skills: formData.required_skills
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean),
      nice_to_have_skills: formData.nice_to_have_skills
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean),
      required_experience_years: formData.required_experience_years
        ? parseInt(formData.required_experience_years)
        : null,
      salary_range_min: formData.salary_range_min
        ? parseFloat(formData.salary_range_min)
        : null,
      salary_range_max: formData.salary_range_max
        ? parseFloat(formData.salary_range_max)
        : null,
    };

    try {
      await jobsAPI.create(payload);
      setShowModal(false);
      setFormData({
        title: '',
        description: '',
        required_skills: '',
        nice_to_have_skills: '',
        required_experience_years: '',
        location: '',
        salary_range_min: '',
        salary_range_max: '',
        department: '',
      });
      fetchJobs();
    } catch (err) {
      setError('Failed to create job');
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this job?')) {
      return;
    }

    try {
      await jobsAPI.delete(id);
      fetchJobs();
    } catch (err) {
      setError('Failed to delete job');
      console.error(err);
    }
  };

  const handleViewDetails = (job) => {
    setSelectedJob(job);
    setShowDetailModal(true);
  };

  return (
    <div className="jobs-page">
      <div className="page-header">
        <div>
          <h1>Job Requisitions</h1>
          <p className="subtitle">Create and manage job positions</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={20} />
          Create Job
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={clearError} style={{ marginLeft: '1rem' }}>×</button>
        </div>
      )}

      {/* Create Job Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal modal-large" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal-close"
              onClick={() => setShowModal(false)}
            >
              ×
            </button>
            <h2>Create New Job</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-row">
                <div className="form-group">
                  <label>Job Title *</label>
                  <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Department</label>
                  <input
                    type="text"
                    name="department"
                    value={formData.department}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Job Description *</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows="4"
                  required
                ></textarea>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Location</label>
                  <input
                    type="text"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="form-group">
                  <label>Years of Experience</label>
                  <input
                    type="number"
                    name="required_experience_years"
                    value={formData.required_experience_years}
                    onChange={handleInputChange}
                    min="0"
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Required Skills (comma-separated)</label>
                <input
                  type="text"
                  name="required_skills"
                  value={formData.required_skills}
                  onChange={handleInputChange}
                  placeholder="e.g., Python, FastAPI, React"
                />
              </div>

              <div className="form-group">
                <label>Nice-to-Have Skills (comma-separated)</label>
                <input
                  type="text"
                  name="nice_to_have_skills"
                  value={formData.nice_to_have_skills}
                  onChange={handleInputChange}
                  placeholder="e.g., Docker, Kubernetes, AWS"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Salary Range Min</label>
                  <input
                    type="number"
                    name="salary_range_min"
                    value={formData.salary_range_min}
                    onChange={handleInputChange}
                    min="0"
                  />
                </div>
                <div className="form-group">
                  <label>Salary Range Max</label>
                  <input
                    type="number"
                    name="salary_range_max"
                    value={formData.salary_range_max}
                    onChange={handleInputChange}
                    min="0"
                  />
                </div>
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Job
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Jobs Grid */}
      <div className="jobs-grid">
        {loading ? (
          <div className="loading-state">
            <div className="loading"></div>
            <p>Loading jobs...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="empty-state">
            <Briefcase size={48} />
            <h3>No jobs yet</h3>
            <p>Start by creating a job requisition</p>
            <button className="btn btn-primary" onClick={() => setShowModal(true)}>
              <Plus size={20} />
              Create First Job
            </button>
          </div>
        ) : (
          jobs.map((job) => (
            <div key={job.id} className="job-card card">
              <div className="job-header">
                <h3>{job.title}</h3>
                <span className={`badge badge-${job.status === 'open' ? 'success' : 'warning'}`}>
                  {job.status}
                </span>
              </div>

              <p className="job-department">{job.department || 'Department N/A'}</p>

              <p className="job-description">{job.description}</p>

              {job.required_skills && (
                <div className="job-skills">
                  <strong>Required Skills:</strong>
                  <div className="skills-list">
                    {job.required_skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>
              )}

              <div className="job-details">
                {job.location && (
                  <span className="detail-item">
                    📍 {job.location}
                  </span>
                )}
                {job.required_experience_years && (
                  <span className="detail-item">
                    📅 {job.required_experience_years}+ years
                  </span>
                )}
                {job.salary_range_min && (
                  <span className="detail-item">
                    💰 ${job.salary_range_min.toLocaleString()} - ${job.salary_range_max?.toLocaleString()}
                  </span>
                )}
              </div>

              <div className="job-actions">
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => handleViewDetails(job)}
                >
                  <Eye size={16} />
                  View
                </button>
                <button
                  className="btn btn-danger btn-sm"
                  onClick={() => handleDelete(job.id)}
                >
                  <Trash2 size={16} />
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Detail Modal */}
      {showDetailModal && selectedJob && (
        <div className="modal-overlay" onClick={() => setShowDetailModal(false)}>
          <div className="modal modal-large" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal-close"
              onClick={() => setShowDetailModal(false)}
            >
              ×
            </button>
            <h2>{selectedJob.title}</h2>

            <div className="detail-content">
              <p className="badge badge-primary" style={{ marginBottom: '1rem' }}>
                Status: {selectedJob.status}
              </p>

              <h3>Job Details</h3>
              <p><strong>Department:</strong> {selectedJob.department || 'N/A'}</p>
              <p><strong>Location:</strong> {selectedJob.location || 'N/A'}</p>
              <p><strong>Experience Required:</strong> {selectedJob.required_experience_years || 'N/A'} years</p>

              <h3 style={{ marginTop: '1.5rem' }}>Description</h3>
              <p>{selectedJob.description}</p>

              {selectedJob.required_skills && (
                <>
                  <h3 style={{ marginTop: '1.5rem' }}>Required Skills</h3>
                  <div className="skills-list">
                    {selectedJob.required_skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </>
              )}

              {selectedJob.nice_to_have_skills && (
                <>
                  <h3 style={{ marginTop: '1.5rem' }}>Nice-to-Have Skills</h3>
                  <div className="skills-list">
                    {selectedJob.nice_to_have_skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag" style={{ backgroundColor: '#fed7aa', color: '#92400e' }}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </>
              )}

              {selectedJob.salary_range_min && (
                <>
                  <h3 style={{ marginTop: '1.5rem' }}>Salary Range</h3>
                  <p>${selectedJob.salary_range_min.toLocaleString()} - ${selectedJob.salary_range_max?.toLocaleString()}</p>
                </>
              )}
            </div>

            <div className="modal-actions">
              <button
                className="btn btn-secondary"
                onClick={() => setShowDetailModal(false)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Placeholder for Briefcase icon if lucide-react doesn't have it
const Briefcase = ({ size = 24 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
    <path d="M16 7v-2a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"></path>
  </svg>
);

export default Jobs;
