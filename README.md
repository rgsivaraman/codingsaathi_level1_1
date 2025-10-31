# Agent Marketplace

A full-featured marketplace for AI agents where users can create, share, fork, and deploy Python-based AI agents.

## 🚀 Features

### User Features
- **User Authentication**: Secure registration and login with JWT tokens
- **Agent Management**: Create, update, delete, and manage your own agents
- **Agent Marketplace**: Browse and search through public agents
- **Forking**: Fork any public agent to create your own version
- **Agent Execution**: Run agents with custom input in a sandboxed environment
- **Ratings & Reviews**: Rate and review agents from the community
- **Versioning**: Track agent versions and fork lineage

### Technical Features
- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React with modern UI/UX
- **Security**: JWT authentication, sandboxed code execution
- **Containerization**: Fully Dockerized application
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## 📋 Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+, Node.js 18+, and PostgreSQL 15+

## 🛠️ Installation & Setup

### Option 1: Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd codingsaathi_level1_1
```

2. Build and start all services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the backend:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## 📖 Usage Guide

### Creating an Agent

1. Register and login to the platform
2. Click "Create Agent" in the navigation
3. Fill in agent details:
   - **Name**: Give your agent a descriptive name
   - **Description**: Explain what your agent does
   - **Code**: Write Python code (use `input_data` for input, set `result` for output)
   - **Tags**: Add comma-separated tags for discoverability
   - **Public**: Choose if your agent should be public

Example agent code:
```python
# Simple text reverser agent
text = input_data.get('text', '')
result = text[::-1]
```

### Using an Agent

1. Browse the marketplace
2. Click on an agent to view details
3. In the "Execute Agent" section:
   - Enter input as JSON (e.g., `{"text": "hello"}`)
   - Click "Execute" to run the agent
4. View the output or any errors

### Forking an Agent

1. Navigate to any public agent
2. Click "Fork Agent" button
3. You now have your own copy to modify and use

### Rating & Reviewing

1. On any agent detail page
2. Select a rating (1-5 stars) and submit
3. Write a review to share your experience

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend (React)              │
│                    Port: 80                     │
└────────────────┬────────────────────────────────┘
                 │
                 │ HTTP/REST API
                 │
┌────────────────▼────────────────────────────────┐
│              Backend (FastAPI)                  │
│                 Port: 8000                      │
│  ┌──────────────────────────────────────────┐  │
│  │  Authentication (JWT)                    │  │
│  │  Agent CRUD Operations                   │  │
│  │  Agent Execution Engine                  │  │
│  │  Ratings & Reviews                       │  │
│  └──────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────┘
                 │
                 │ SQLAlchemy ORM
                 │
┌────────────────▼────────────────────────────────┐
│            PostgreSQL Database                  │
│                Port: 5432                       │
│  ┌──────────────────────────────────────────┐  │
│  │  Users, Agents, Ratings, Reviews         │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 🔒 Security

- **Authentication**: JWT tokens with configurable expiration
- **Password Hashing**: bcrypt for secure password storage
- **Code Execution**: Sandboxed Python execution with restricted builtins
  - **Note**: The current sandboxing is suitable for trusted environments. For production use with untrusted code, implement proper containerized execution using Docker containers or similar isolation mechanisms.
- **CORS**: Configurable allowed origins
- **SQL Injection**: Protected via SQLAlchemy ORM
- **Secret Key**: Auto-generated unique key per deployment (override via environment variable for production)

## 📚 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

#### Agents
- `GET /agents/` - List all public agents (with search/filter)
- `GET /agents/{id}` - Get agent details
- `POST /agents/` - Create new agent
- `PUT /agents/{id}` - Update agent
- `DELETE /agents/{id}` - Delete agent (soft delete)
- `POST /agents/{id}/fork` - Fork an agent
- `POST /agents/execute` - Execute agent code
- `GET /agents/my-agents` - Get current user's agents

#### Ratings & Reviews
- `POST /api/ratings` - Create/update rating
- `GET /api/agents/{id}/ratings` - Get agent ratings
- `POST /api/reviews` - Create review
- `GET /api/agents/{id}/reviews` - Get agent reviews
- `PUT /api/reviews/{id}` - Update review
- `DELETE /api/reviews/{id}` - Delete review

## 🚀 Deployment

### Docker Deployment

The application is fully containerized and can be deployed to any platform supporting Docker:

1. **Docker Compose (Local/VPS)**:
```bash
docker-compose up -d
```

2. **Heroku**:
```bash
# Install Heroku CLI
heroku container:login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku container:push web
heroku container:release web
```

3. **AWS ECS/Fargate**:
- Use the provided Dockerfiles
- Set up RDS PostgreSQL
- Configure environment variables

4. **Google Cloud Run**:
```bash
gcloud run deploy agent-marketplace --source .
```

### Environment Variables

Production environment variables to configure:

```bash
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_ORIGINS=https://your-domain.com
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
REACT_APP_API_URL=https://api.your-domain.com
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🛣️ Roadmap

- [ ] OAuth integration (Google, GitHub)
- [ ] Email notifications for agent updates
- [ ] Analytics dashboard
- [ ] Advanced search with Elasticsearch
- [ ] Agent collaboration features
- [ ] Webhook support for agent deployment
- [ ] CI/CD pipeline integration
- [ ] Monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 👥 Support

For issues and questions:
- Create an issue in the repository
- Contact: [your-email@example.com]

## 🎉 Acknowledgments

- FastAPI for the excellent web framework
- React for the frontend library
- PostgreSQL for reliable data storage
- Docker for containerization
