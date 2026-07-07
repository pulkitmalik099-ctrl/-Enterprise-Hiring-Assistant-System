import React, { useState, useEffect } from 'react';
import { Upload, Plus, Trash2, Eye, Download } from 'lucide-react';
import { candidatesAPI, workflowsAPI } from '../services/api';
import { useLoading, useError } from '../utils/hooks';
import './Candidates.css';

const Candidates = () => {
  const [candidates, setCandidates] = useState([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const { loading, setLoading } = useLoading();
  const { error, setError, clearError } = useError();
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      const response = await candidatesAPI.list(0, 50);
      setCandidates(response.data || []);
      clearError();
    } catch (err) {
      setError('Failed to load candidates');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!uploadFile) {
      setError('Please select a file');
      return;
    }

    try {
      setUploading(true);
      const response = await candidatesAPI.upload(uploadFile);

      if (response.data.analysis.success) {
        setShowUploadModal(false);
        setUploadFile(null);
        fetchCandidates();
      } else {
        setError(response.data.analysis.error || 'Upload failed');
      }
    } catch (err) {
      setError('Failed to upload resume');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this candidate?')) {
      return;
    }

    try {
      await candidatesAPI.delete(id);
      fetchCandidates();
    } catch (err) {
      setError('Failed to delete candidate');
      console.error(err);
    }
  };

  const handleViewDetails = (candidate) => {
    setSelectedCandidate(candidate);
    setShowDetailModal(true);
  };

  const getStatusBadgeColor = (status) => {
    switch (status) {
      case 'submitted':
        return 'badge-info';
      case 'reviewed':
        return 'badge-primary';
      case 'shortlisted':
        return 'badge-success';
      case 'rejected':
        return 'badge-danger';
      default:
        return 'badge-warning';
    }
  };

  return (
    <div className="candidates-page">
      <div className="page-header">
        <div>
          <h1>Candidates</h1>
          <p className="subtitle">Manage and analyze candidate resumes</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowUploadModal(true)}>
          <Upload size={20} />
          Upload Resume
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={clearError} style={{ marginLeft: '1rem' }}>×</button>
        </div>
      )}

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="modal-overlay" onClick={() => setShowUploadModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Upload Resume</h2>
            <form onSubmit={handleFileUpload}>
              <div className="form-group">
                <label>Select PDF or DOCX file</label>
                <input
                  type="file"
                  accept=".pdf,.docx,.doc"
                  onChange={(e) => setUploadFile(e.target.files[0])}
                  required
                />
                {uploadFile && <p className="file-name">{uploadFile.name}</p>}
              </div>
              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowUploadModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={uploading}
                >
                  {uploading ? 'Uploading...' : 'Upload & Analyze'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Candidates Table */}
      <div className="card">
        {loading ? (
          <div className="loading-state">
            <div className="loading"></div>
            <p>Loading candidates...</p>
          </div>
        ) : candidates.length === 0 ? (
          <div className="empty-state">
            <Upload size={48} />
            <h3>No candidates yet</h3>
            <p>Start by uploading resumes to analyze candidates</p>
            <button className="btn btn-primary" onClick={() => setShowUploadModal(true)}>
              <Upload size={20} />
              Upload First Resume
            </button>
          </div>
        ) : (
          <div className="candidates-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Quality Score</th>
                  <th>Location</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {candidates.map((candidate) => (
                  <tr key={candidate.id}>
                    <td className="name-cell">{candidate.name}</td>
                    <td>{candidate.email}</td>
                    <td>
                      <span className={`badge ${getStatusBadgeColor(candidate.status)}`}>
                        {candidate.status}
                      </span>
                    </td>
                    <td>
                      <div className="score-bar">
                        <div
                          className="score-fill"
                          style={{
                            width: `${candidate.quality_score || 0}%`,
                            backgroundColor:
                              (candidate.quality_score || 0) > 75
                                ? '#10b981'
                                : (candidate.quality_score || 0) > 50
                                ? '#f59e0b'
                                : '#ef4444',
                          }}
                        ></div>
                        <span className="score-text">
                          {Math.round(candidate.quality_score || 0)}%
                        </span>
                      </div>
                    </td>
                    <td>{candidate.location || 'N/A'}</td>
                    <td>
                      <div className="action-buttons">
                        <button
                          className="btn-icon"
                          onClick={() => handleViewDetails(candidate)}
                          title="View Details"
                        >
                          <Eye size={18} />
                        </button>
                        <button
                          className="btn-icon danger"
                          onClick={() => handleDelete(candidate.id)}
                          title="Delete"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Detail Modal */}
      {showDetailModal && selectedCandidate && (
        <div className="modal-overlay" onClick={() => setShowDetailModal(false)}>
          <div className="modal modal-large" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal-close"
              onClick={() => setShowDetailModal(false)}
            >
              ×
            </button>
            <h2>{selectedCandidate.name}</h2>

            <div className="detail-grid">
              <div className="detail-section">
                <h3>Contact Information</h3>
                <p><strong>Email:</strong> {selectedCandidate.email}</p>
                <p><strong>Phone:</strong> {selectedCandidate.phone || 'N/A'}</p>
                <p><strong>Location:</strong> {selectedCandidate.location || 'N/A'}</p>
              </div>

              {selectedCandidate.parsed_data && (
                <>
                  <div className="detail-section">
                    <h3>Skills</h3>
                    <div className="skills-list">
                      {selectedCandidate.parsed_data.skills?.map((skill, idx) => (
                        <span key={idx} className="skill-tag">{skill}</span>
                      ))}
                    </div>
                  </div>

                  <div className="detail-section">
                    <h3>Experience</h3>
                    {selectedCandidate.parsed_data.experience?.map((exp, idx) => (
                      <div key={idx} className="experience-item">
                        <p><strong>{exp.title}</strong> at {exp.company}</p>
                        <p className="text-light">{exp.duration}</p>
                        <p>{exp.description}</p>
                      </div>
                    ))}
                  </div>

                  <div className="detail-section">
                    <h3>Education</h3>
                    {selectedCandidate.parsed_data.education?.map((edu, idx) => (
                      <div key={idx} className="education-item">
                        <p><strong>{edu.degree}</strong> in {edu.field}</p>
                        <p className="text-light">{edu.institution}</p>
                      </div>
                    ))}
                  </div>
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

export default Candidates;
