# Quick Deployment Guide - Step by Step

This is the easiest way to deploy your Agent Marketplace online for free.

## What You'll Need
- A GitHub account
- 10 minutes of your time
- No credit card required!

---

## Step 1: Choose Your Deployment Method

I recommend **Railway.app** because it's the simplest - everything in one place.

---

## Method A: Railway.app (Recommended - Easiest)

### 1. Sign Up
- Go to [Railway.app](https://railway.app)
- Click "Login" → "Login with GitHub"
- Authorize Railway to access your GitHub

### 2. Create New Project
- Click "New Project" button
- Select "Deploy from GitHub repo"
- Find and select `rgsivaraman/codingsaathi_level1_1`
- Railway will start setting up

### 3. Add Database
- In your Railway project dashboard, click "+ New"
- Select "Database" → "PostgreSQL"
- Wait for it to deploy (1-2 minutes)

### 4. Configure Backend
- Click on the "backend" service in Railway
- Go to "Variables" tab
- Click "Add Variable" and add these:

```
DATABASE_URL = ${{Postgres.DATABASE_URL}}
SECRET_KEY = (click "Generate" button to auto-generate)
ALLOWED_ORIGINS = *
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

- Go to "Settings" tab
- Scroll to "Networking" → Click "Generate Domain"
- **Copy this URL** - you'll need it! (Example: `backend-production-abc123.up.railway.app`)

### 5. Configure Frontend
- Click on the "frontend" service
- Go to "Variables" tab
- Add this variable:

```
REACT_APP_API_URL = https://YOUR-BACKEND-URL-FROM-STEP-4
```

- Go to "Settings" → "Networking" → "Generate Domain"
- **This is your app URL!**

### 6. Update CORS (Important!)
- Go back to the backend service
- Click on "Variables" tab
- Edit `ALLOWED_ORIGINS` and change `*` to your frontend URL
- Example: `https://frontend-production-xyz456.up.railway.app`

### 7. Wait for Deployment
- Railway will automatically deploy everything
- Wait 5-10 minutes for the first deployment
- Watch the "Deployments" tab for progress

### 8. Access Your App! 🎉
- Visit your frontend URL from Step 5
- Your Agent Marketplace is now live!

---

## Method B: Render.com (Alternative)

### 1. Sign Up
- Go to [Render.com](https://render.com)
- Sign up with GitHub

### 2. Fork This Repository
- Go to the GitHub repository
- Click "Fork" button (top right)
- This creates your own copy

### 3. Create Blueprint
- In Render dashboard, click "New +"
- Select "Blueprint"
- Connect your forked repository
- Render will read the `render.yaml` file

### 4. Review Services
- Render will show: Backend, Frontend, Database
- Click "Apply"
- Wait 10-15 minutes for deployment

### 5. Get Your URLs
- Go to "Dashboard"
- Click on "frontend" service
- Copy the URL - this is your app!

---

## Method C: Using the Script (For Developers)

If you have the repository cloned locally:

```bash
# Install Railway CLI
curl -fsSL cli.new | sh

# Login to Railway
railway login

# Deploy
./deploy-online.sh
```

---

## Troubleshooting

### "Backend won't start"
- Check that DATABASE_URL is set correctly
- Make sure PostgreSQL database is created
- Check logs in the platform dashboard

### "Frontend shows blank page"
- Verify REACT_APP_API_URL is set
- Check browser console for errors
- Make sure backend URL is correct

### "Can't connect to backend"
- Update ALLOWED_ORIGINS in backend to match frontend URL
- Wait a few minutes after changing environment variables
- Check backend is running (visit `/health` endpoint)

---

## Free Tier Limits

**Railway:**
- $5 free credit/month
- Usually enough for this app
- No credit card needed to start

**Render:**
- 750 hours/month free
- Spins down after 15 min idle
- Free tier available

---

## Next Steps After Deployment

1. **Register an Account**: Visit your app and create your first user
2. **Create Your First Agent**: Try the text reverser example
3. **Share Your App**: Send the URL to friends!
4. **Monitor Usage**: Check the platform dashboard

---

## Need Help?

1. Check the logs in Railway/Render dashboard
2. See [DEPLOY_ONLINE.md](DEPLOY_ONLINE.md) for detailed troubleshooting
3. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (coming soon)

---

## Video Tutorial (Coming Soon)

Watch a step-by-step video walkthrough at: [Link to be added]

---

## Success Checklist

- [ ] Signed up for Railway/Render
- [ ] Created new project from GitHub repo
- [ ] Added PostgreSQL database
- [ ] Set backend environment variables
- [ ] Set frontend environment variables
- [ ] Generated domains for both services
- [ ] Updated CORS settings
- [ ] Waited for deployment (5-10 min)
- [ ] Visited app URL and it works!

**Congratulations! Your Agent Marketplace is now live online! 🚀**
