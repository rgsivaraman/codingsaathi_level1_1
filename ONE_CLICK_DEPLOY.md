# One-Click Deploy Buttons

Deploy the Agent Marketplace with one click:

## Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/-PqHHD?referralCode=alphasec)

**What gets deployed:**
- Backend API (FastAPI)
- PostgreSQL Database
- Automatic environment variables

**After deployment:**
1. Get your backend URL from Railway dashboard
2. Deploy frontend to Vercel (see below)
3. Update ALLOWED_ORIGINS in Railway backend settings

---

## Deploy Frontend to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/rgsivaraman/codingsaathi_level1_1&project-name=agent-marketplace&root-directory=frontend&env=REACT_APP_API_URL)

**Environment Variables Required:**
- `REACT_APP_API_URL`: Your Railway backend URL

---

## Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/rgsivaraman/codingsaathi_level1_1)

Uses the `render.yaml` blueprint to deploy:
- Backend service
- Frontend service
- PostgreSQL database

---

## Manual Deployment

If the buttons don't work, follow the detailed guide in [DEPLOY_ONLINE.md](DEPLOY_ONLINE.md).

---

## Quick Setup Steps

### 1. Deploy Backend to Railway

```bash
# Install Railway CLI
curl -fsSL cli.new | sh

# Login
railway login

# Deploy
cd /path/to/codingsaathi_level1_1
./deploy-online.sh
```

### 2. Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Set environment variable
vercel env add REACT_APP_API_URL production
# Enter your Railway backend URL
```

### 3. Update CORS

In Railway dashboard:
- Go to backend service
- Add environment variable:
  - `ALLOWED_ORIGINS`: `https://your-vercel-app.vercel.app`
- Redeploy

---

## Free Tier Resources

**Railway:**
- $5 free credit/month
- Enough for backend + database
- No credit card required initially

**Vercel:**
- Unlimited personal projects
- 100GB bandwidth/month
- Free SSL certificates

**Render:**
- 750 hours/month free
- Free PostgreSQL database
- Free SSL certificates

---

## Support

If you encounter issues:
1. Check [DEPLOY_ONLINE.md](DEPLOY_ONLINE.md) for troubleshooting
2. Review platform-specific logs
3. Open an issue in the repository

---

## Demo

Once deployed, you'll have:
- ✅ Live marketplace at `https://your-app.vercel.app`
- ✅ API at `https://your-app.railway.app`
- ✅ Auto-generated SSL certificates
- ✅ Automatic deployments on git push
- ✅ Global CDN distribution (Vercel)

Estimated deployment time: **5-10 minutes**
