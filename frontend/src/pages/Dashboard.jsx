import React, { useEffect, useState } from 'react';
import { PieChart, Pie, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { Users, Briefcase, TrendingUp, CheckCircle } from 'lucide-react';
import { candidatesAPI, jobsAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalCandidates: 0,
    totalJobs: 0,
    activeJobs: 0,
    successRate: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [candidatesRes, jobsRes] = await Promise.all([
          candidatesAPI.list(0, 1),
          jobsAPI.list('open', 0, 1),
        ]);

        setStats({
          totalCandidates: candidatesRes.data.length || 0,
          totalJobs: jobsRes.data.length || 0,
          activeJobs: jobsRes.data.filter(j => j.status === 'open').length || 0,
          successRate: 85,
        });
        setError(null);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className={`stat-card ${color}`}>
      <div className="stat-icon">
        <Icon size={24} />
      </div>
      <div className="stat-content">
        <p className="stat-label">{label}</p>
        <p className="stat-value">{value}</p>
      </div>
    </div>
  );

  const candidateStatusData = [
    { name: 'Submitted', value: 30 },
    { name: 'Reviewed', value: 25 },
    { name: 'Shortlisted', value: 20 },
    { name: 'Interviewed', value: 15 },
    { name: 'Offered', value: 10 },
  ];

  const matchScoreData = [
    { name: 'Week 1', score: 72 },
    { name: 'Week 2', score: 75 },
    { name: 'Week 3', score: 78 },
    { name: 'Week 4', score: 82 },
    { name: 'Week 5', score: 85 },
  ];

  const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <p className="subtitle">Welcome back! Here's your hiring overview.</p>

      {error && <div className="alert alert-error">{error}</div>}

      {/* Stats Cards */}
      <div className="stats-grid">
        <StatCard icon={Users} label="Total Candidates" value={stats.totalCandidates} color="blue" />
        <StatCard icon={Briefcase} label="Total Jobs" value={stats.totalJobs} color="green" />
        <StatCard icon={TrendingUp} label="Active Jobs" value={stats.activeJobs} color="orange" />
        <StatCard icon={CheckCircle} label="Success Rate" value={`${stats.successRate}%`} color="purple" />
      </div>

      {/* Charts */}
      <div className="charts-grid">
        {/* Candidate Status Distribution */}
        <div className="chart-container">
          <h3>Candidate Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={candidateStatusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {candidateStatusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Average Match Score Trend */}
        <div className="chart-container">
          <h3>Average Match Score Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={matchScoreData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="score"
                stroke="#2563eb"
                strokeWidth={2}
                dot={{ fill: '#2563eb' }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="recent-activity">
        <h3>Recent Activity</h3>
        <div className="activity-list">
          <div className="activity-item">
            <div className="activity-indicator"></div>
            <div className="activity-content">
              <p className="activity-title">New candidate uploaded</p>
              <p className="activity-time">2 hours ago</p>
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-indicator"></div>
            <div className="activity-content">
              <p className="activity-title">Job matching completed</p>
              <p className="activity-time">4 hours ago</p>
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-indicator"></div>
            <div className="activity-content">
              <p className="activity-title">Interview feedback generated</p>
              <p className="activity-time">1 day ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
