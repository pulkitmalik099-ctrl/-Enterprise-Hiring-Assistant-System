# Enterprise Hiring Assistant - Frontend

A modern React dashboard for managing the AI-powered hiring assistant system.

## Features

- 📊 **Dashboard** - Overview of hiring metrics and activity
- 👥 **Candidates** - Manage and analyze candidate resumes
- 💼 **Jobs** - Create and manage job requisitions
- 🤖 **Workflows** - Execute AI agent pipelines
- 📈 **Analytics** - Visualize hiring data and trends
- 🎨 **Responsive Design** - Works on desktop, tablet, and mobile

## Tech Stack

- **React 18** - UI framework
- **React Router v6** - Navigation
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **CSS3** - Styling

## Quick Start

### Prerequisites

- Node.js 14+
- npm or yarn

### Installation

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create environment file:**
```bash
cp .env.example .env
```

4. **Update API URL (optional):**
Edit `.env` if your backend is not on `localhost:8000`:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Running Development Server

```bash
npm start
```

- Opens http://localhost:3000 in browser
- Hot reload on file changes
- Errors display in terminal and browser console

### Building for Production

```bash
npm run build
```

- Optimized build in `build/` directory
- Ready for deployment

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Layout.jsx       # Main layout with sidebar
│   │   └── Layout.css
│   ├── pages/               # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Candidates.jsx
│   │   ├── Jobs.jsx
│   │   ├── Workflows.jsx
│   │   └── *.css
│   ├── services/            # API integration
│   │   └── api.js           # Axios API client
│   ├── utils/               # Utility functions
│   │   └── hooks.js         # Custom React hooks
│   ├── styles/              # Global styles
│   │   └── App.css
│   ├── App.jsx              # Main app component
│   └── index.jsx            # Entry point
├── public/
│   └── index.html           # HTML template
├── package.json
└── README.md
```

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000/api`.

### Available Endpoints

**Candidates:**
- `GET /candidates/` - List candidates
- `POST /candidates/analyze` - Analyze resume
- `POST /candidates/upload` - Upload resume file
- `GET /candidates/{id}` - Get candidate details
- `PUT /candidates/{id}` - Update candidate
- `DELETE /candidates/{id}` - Delete candidate

**Jobs:**
- `GET /jobs/` - List jobs
- `POST /jobs/` - Create job
- `GET /jobs/{id}` - Get job details
- `PUT /jobs/{id}` - Update job
- `DELETE /jobs/{id}` - Delete job
- `POST /jobs/{id}/match-candidates` - Match candidates

**Workflows:**
- `POST /workflows/analyze-resume` - Analyze resume with job matching
- `POST /workflows/interview-feedback` - Generate interview feedback
- `POST /workflows/full-pipeline` - Execute complete pipeline
- `POST /workflows/agent/{agent_name}` - Execute specific agent

## Pages Overview

### Dashboard
Displays key metrics:
- Total candidates
- Total jobs
- Active positions
- Success rate
- Charts and visualizations
- Recent activity feed

### Candidates
Manage candidate resumes:
- Upload and analyze resumes
- View candidate details
- Display parsed resume data
- Quality score visualization
- Resume analysis results

### Jobs
Manage job requisitions:
- Create new job openings
- View job details
- Specify required skills
- Set salary ranges
- Manage job status

### Workflows
Execute AI pipelines:
- Full hiring pipeline execution
- Resume analysis
- Job matching
- Interview prep generation
- Agent information
- Results visualization

## Customization

### Colors

Edit `src/styles/App.css` to change the color scheme:

```css
:root {
  --primary-color: #2563eb;     /* Change this */
  --secondary-color: #10b981;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  /* ... more colors */
}
```

### Styling

- Global styles: `src/styles/App.css`
- Component styles: `src/components/*.css`, `src/pages/*.css`
- Uses CSS custom properties (variables)
- Responsive design with media queries

## Deployment

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
npm run build
# Then drag-and-drop 'build' folder to Netlify
```

### Docker

Create a `Dockerfile` in frontend directory:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t hiring-frontend .
docker run -p 3000:3000 hiring-frontend
```

## Environment Variables

Create `.env` file:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api

# Optional: Add more as needed
REACT_APP_DEBUG=false
```

## Performance Tips

1. **Code Splitting** - Routes use lazy loading
2. **Image Optimization** - Use SVG icons (Lucide)
3. **Caching** - Browser caches API responses
4. **Minification** - Build process minifies code
5. **Bundle Analysis** - Run `npm run build` to see size

## Troubleshooting

### API Connection Issues

**Problem:** "Failed to load candidates"

**Solution:**
1. Check backend is running on `localhost:8000`
2. Verify API URL in `.env`
3. Check browser console for CORS errors
4. Enable CORS in FastAPI backend

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### Build Fails

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [project-repo/issues](https://github.com/pulkitmalik099-ctrl/Enterprise-Hiring-Assistant-System/issues)
- Email: support@example.com

## Roadmap

- [ ] User authentication
- [ ] Real-time notifications
- [ ] Advanced filtering and search
- [ ] Export to PDF/CSV
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Mobile app

---

**Last Updated:** 2026-07-08
