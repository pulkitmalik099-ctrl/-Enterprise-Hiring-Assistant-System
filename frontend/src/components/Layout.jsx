import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, Home, Users, Briefcase, Settings, LogOut } from 'lucide-react';
import './Layout.css';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(true);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/candidates', label: 'Candidates', icon: Users },
    { path: '/jobs', label: 'Jobs', icon: Briefcase },
    { path: '/workflows', label: 'Workflows', icon: Settings },
  ];

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className={`sidebar ${!sidebarOpen ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <h1 className="logo">🚀 Hiring AI</h1>
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <Menu size={20} />
          </button>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
              >
                <Icon size={20} />
                {sidebarOpen && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <button className="nav-item logout">
            <LogOut size={20} />
            {sidebarOpen && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <h2>Enterprise Hiring Assistant</h2>
            <div className="header-actions">
              <span className="status-indicator"></span>
              <span className="status-text">Connected</span>
            </div>
          </div>
        </header>

        {/* Content */}
        <div className="content">
          {children}
        </div>

        {/* Footer */}
        <footer className="footer">
          <p>© 2026 Enterprise Hiring Assistant. All rights reserved.</p>
        </footer>
      </main>
    </div>
  );
};

export default Layout;
