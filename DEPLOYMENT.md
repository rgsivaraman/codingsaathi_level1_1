# Deployment Guide for Agent Marketplace

This guide covers multiple deployment options for the Agent Marketplace application.

## Table of Contents
1. [Quick Start with Docker](#quick-start-with-docker)
2. [Heroku Deployment](#heroku-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Google Cloud Deployment](#google-cloud-deployment)
5. [Production Considerations](#production-considerations)

## Quick Start with Docker

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd codingsaathi_level1_1
```

2. Run the deployment script:
```bash
./deploy.sh
```

Or manually:
```bash
docker-compose up --build -d
```

3. Access the application:
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Environment Configuration

Edit `docker-compose.yml` or create `.env` file:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/agent_marketplace
SECRET_KEY=<generate-a-secure-secret-key>
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:80
```

## Heroku Deployment

### Backend Deployment

1. Install Heroku CLI:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Login to Heroku:
```bash
heroku login
```

3. Create Heroku app:
```bash
cd backend
heroku create agent-marketplace-backend
```

4. Add PostgreSQL:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. Set environment variables:
```bash
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set ALLOWED_ORIGINS=https://your-frontend-url.com
```

6. Create `Procfile` in backend directory:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

7. Deploy:
```bash
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a agent-marketplace-backend
git push heroku main
```

### Frontend Deployment

1. Create Heroku app for frontend:
```bash
cd frontend
heroku create agent-marketplace-frontend
```

2. Add buildpack:
```bash
heroku buildpacks:set mars/create-react-app
```

3. Set API URL:
```bash
heroku config:set REACT_APP_API_URL=https://agent-marketplace-backend.herokuapp.com
```

4. Deploy:
```bash
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a agent-marketplace-frontend
git push heroku main
```

## AWS Deployment

### Using AWS ECS with Fargate

1. **Setup AWS CLI**:
```bash
pip install awscli
aws configure
```

2. **Create RDS PostgreSQL Instance**:
```bash
aws rds create-db-instance \
    --db-instance-identifier agent-marketplace-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password <your-password> \
    --allocated-storage 20
```

3. **Create ECR Repositories**:
```bash
aws ecr create-repository --repository-name agent-marketplace-backend
aws ecr create-repository --repository-name agent-marketplace-frontend
```

4. **Build and Push Docker Images**:
```bash
# Backend
cd backend
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t agent-marketplace-backend .
docker tag agent-marketplace-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/agent-marketplace-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/agent-marketplace-backend:latest

# Frontend
cd ../frontend
docker build -t agent-marketplace-frontend .
docker tag agent-marketplace-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/agent-marketplace-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/agent-marketplace-frontend:latest
```

5. **Create ECS Cluster and Task Definitions** using AWS Console or CloudFormation

6. **Create Application Load Balancer** to route traffic

7. **Configure Environment Variables** in ECS Task Definitions

## Google Cloud Deployment

### Using Cloud Run

1. **Install Google Cloud SDK**:
```bash
curl https://sdk.cloud.google.com | bash
gcloud init
```

2. **Enable APIs**:
```bash
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

3. **Create Cloud SQL PostgreSQL Instance**:
```bash
gcloud sql instances create agent-marketplace-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1
```

4. **Deploy Backend**:
```bash
cd backend
gcloud run deploy agent-marketplace-backend \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars DATABASE_URL=<cloud-sql-connection-string>,SECRET_KEY=<secret>
```

5. **Deploy Frontend**:
```bash
cd frontend
gcloud run deploy agent-marketplace-frontend \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars REACT_APP_API_URL=<backend-url>
```

## Production Considerations

### Security

1. **Change Default Secrets**:
```bash
# Generate strong secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Enable HTTPS**:
- Use Let's Encrypt for free SSL certificates
- Configure reverse proxy (nginx/traefik)

3. **Set Proper CORS Origins**:
```bash
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

4. **Database Security**:
- Use strong passwords
- Enable SSL for database connections
- Restrict database access by IP

### Performance

1. **Database Connection Pooling**:
Edit `backend/app/core/database.py`:
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

2. **Enable Caching**:
- Redis for session/token caching
- CDN for static assets

3. **Load Balancing**:
- Multiple backend instances
- Use load balancer (AWS ALB, GCP Load Balancer, nginx)

### Monitoring

1. **Application Monitoring**:
- Sentry for error tracking
- New Relic or DataDog for APM

2. **Logging**:
```python
# Add to backend/app/main.py
import logging
logging.basicConfig(level=logging.INFO)
```

3. **Health Checks**:
Already implemented at `/health` endpoint

### Backup

1. **Database Backups**:
```bash
# PostgreSQL backup
pg_dump -h localhost -U postgres agent_marketplace > backup.sql

# Restore
psql -h localhost -U postgres agent_marketplace < backup.sql
```

2. **Automated Backups**:
- AWS RDS automated backups
- Cloud SQL automated backups
- Cron job for custom backups

### Scaling

1. **Horizontal Scaling**:
- Multiple backend/frontend instances
- Container orchestration (Kubernetes, ECS)

2. **Database Scaling**:
- Read replicas for read-heavy workloads
- Connection pooling
- Query optimization

### Environment Variables Template

Create `.env.production`:
```bash
# Backend
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=<strong-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://yourdomain.com
DOCKER_TIMEOUT=30

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
```

## Maintenance

### Update Application:
```bash
git pull origin main
docker-compose build
docker-compose up -d
```

### View Logs:
```bash
docker-compose logs -f
```

### Database Migrations:
```bash
docker-compose exec backend alembic upgrade head
```

### Backup Database:
```bash
docker-compose exec db pg_dump -U postgres agent_marketplace > backup.sql
```

## Troubleshooting

### Backend not starting:
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Check logs: `docker-compose logs backend`

### Frontend not connecting to backend:
- Verify REACT_APP_API_URL is set correctly
- Check CORS settings in backend
- Check browser console for errors

### Database connection errors:
- Verify database credentials
- Check database is accessible
- Ensure database exists

## Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Review environment variables
3. Create an issue in the repository
