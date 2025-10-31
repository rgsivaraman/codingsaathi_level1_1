# Online Deployment Guide

This guide will help you deploy the Agent Marketplace to free online hosting platforms.

## Recommended Free Deployment Stack

**Frontend**: Vercel (Free tier)
**Backend**: Railway.app (Free tier - $5 credit/month)
**Database**: Railway PostgreSQL (Included)

---

## Option 1: Railway.app (Easiest - All in One)

Railway offers $5/month free credit which is enough for this application.

### Steps:

1. **Sign up at [Railway.app](https://railway.app)** with your GitHub account

2. **Create a new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select this repository
   - Railway will auto-detect the services

3. **Add PostgreSQL**:
   - In your project, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically create the database

4. **Configure Backend Service**:
   - Click on the backend service
   - Go to "Variables" tab
   - Add these environment variables:
     ```
     DATABASE_URL=${{Postgres.DATABASE_URL}}
     SECRET_KEY=<click "Generate" to auto-generate>
     ALLOWED_ORIGINS=https://your-frontend-url.up.railway.app
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```
   - Go to "Settings" → "Domains" → Click "Generate Domain"
   - Copy the backend URL for later

5. **Configure Frontend Service**:
   - Click on the frontend service (or add it if needed)
   - Go to "Variables" tab
   - Add:
     ```
     REACT_APP_API_URL=<your-backend-url>
     ```
   - Go to "Settings" → "Domains" → Click "Generate Domain"

6. **Deploy**:
   - Railway will automatically deploy both services
   - Wait 5-10 minutes for the build
   - Access your frontend URL to use the app!

### Railway Project Structure

Create separate services for:
- Backend (backend folder)
- Frontend (frontend folder)
- PostgreSQL (Railway managed)

---

## Option 2: Render.com (Alternative)

Render also offers free tier hosting.

### Steps:

1. **Sign up at [Render.com](https://render.com)** with GitHub

2. **Fork this repository** to your GitHub account

3. **Click "New +"** in Render dashboard

4. **Select "Blueprint"** and connect your forked repository

5. **Render will read render.yaml** and set up all services automatically

6. **Update environment variables**:
   - Go to each service and update the URLs to match your deployed services

7. **Wait for deployment** (5-10 minutes)

The `render.yaml` file in this repository is pre-configured for deployment.

---

## Option 3: Vercel (Frontend) + Railway (Backend)

This combines the best free tiers.

### Backend on Railway:

1. Sign up at Railway.app
2. Create new project from GitHub
3. Select only the `/backend` folder
4. Add PostgreSQL database
5. Set environment variables (as shown in Option 1)
6. Generate domain and copy URL

### Frontend on Vercel:

1. Sign up at [Vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure build settings:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Add Environment Variable:
   - `REACT_APP_API_URL` = `<your-railway-backend-url>`
6. Click "Deploy"

---

## Option 4: Heroku (Traditional)

See DEPLOYMENT.md for detailed Heroku instructions.

Note: Heroku no longer has a free tier but offers student credits.

---

## Post-Deployment Steps

### 1. Update CORS Settings

Once deployed, update the backend's ALLOWED_ORIGINS:
- In Railway/Render, go to backend service
- Update `ALLOWED_ORIGINS` to include your frontend URL
- Redeploy if needed

### 2. Test the Application

1. Visit your frontend URL
2. Register a new account
3. Create a test agent
4. Execute the agent
5. Rate and review

### 3. Custom Domain (Optional)

Both Railway and Render support custom domains:
- Go to service settings
- Add your custom domain
- Update DNS records as instructed

---

## Troubleshooting

### Backend won't start:
- Check DATABASE_URL is set correctly
- Check logs in the platform dashboard
- Ensure all environment variables are set

### Frontend can't connect to backend:
- Verify REACT_APP_API_URL is correct
- Check CORS settings in backend
- Check backend is running (visit /health endpoint)

### Database connection errors:
- Ensure DATABASE_URL format is correct
- Check database service is running
- Verify database is in same region/network

---

## Environment Variables Reference

### Backend:
```
DATABASE_URL=<provided-by-railway-or-render>
SECRET_KEY=<generate-random-string>
ALLOWED_ORIGINS=<your-frontend-url>
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

### Frontend:
```
REACT_APP_API_URL=<your-backend-url>
```

---

## Free Tier Limits

**Railway**:
- $5 credit/month (usually enough for this app)
- 512MB RAM per service
- Sleeps after inactivity

**Render**:
- Free tier for web services
- Spins down after 15 min of inactivity
- 750 hours/month

**Vercel**:
- 100GB bandwidth/month
- Unlimited deployments
- No sleep/downtime

---

## Estimated Monthly Costs

With free tiers: **$0**
- Railway free credit covers backend + database
- Vercel is completely free for personal projects
- Render free tier for less critical services

---

## Next Steps

After successful deployment:
1. Share your app URL!
2. Monitor usage in platform dashboards
3. Set up custom domain if desired
4. Add more agents to the marketplace
5. Invite users to try it out

For production use, consider upgrading to paid tiers for:
- Always-on services (no sleep)
- More resources
- Better performance
- SLA guarantees
