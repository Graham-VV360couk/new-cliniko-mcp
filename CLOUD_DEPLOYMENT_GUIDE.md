# 🚀 Cloud Deployment Guide - Cliniko MCP Server

## 🎯 Overview

This guide provides step-by-step instructions for deploying your Cliniko MCP server to various cloud platforms so your Eleven Labs conversational AI can connect to it.

## 📋 Prerequisites

### Environment Variables
Create a `.env` file in your project root:
```bash
CLINIKO_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
```

### Required Files
- ✅ `main.py` (updated for production)
- ✅ `Dockerfile` (created)
- ✅ `requirements.txt` (exists)
- ✅ `cliniko_client.py` (updated)
- ✅ Tools modules (updated)

## 🐳 Option 1: Docker + Cloud Platform (Recommended)

### Step 1: Test Locally with Docker
```bash
# Build and test locally
cd cliniko_mcp_server
docker build -t cliniko-mcp .
docker run -p 8000:8000 --env-file .env cliniko-mcp

# Test health endpoint
curl http://localhost:8000/health
```

### Step 2: Deploy to Docker Hub
```bash
# Tag and push to Docker Hub
docker tag cliniko-mcp yourusername/cliniko-mcp:latest
docker push yourusername/cliniko-mcp:latest
```

## ☁️ Option 2: Railway (Easiest - Recommended for Beginners)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up and create a new project

### Step 2: Deploy from GitHub
```bash
# Install Railway CLI
npm install -g @railway/cli
railway login

# Deploy
railway init
railway up
```

### Step 3: Configure Environment Variables
```bash
railway variables set CLINIKO_API_KEY=your_api_key_here
railway variables set HOST=0.0.0.0
railway variables set PORT=8000
```

### Step 4: Get Your Deployment URL
Railway will provide a URL like: `https://cliniko-mcp-production.up.railway.app`

## 🐙 Option 3: Render (Free Tier Available)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository

### Step 2: Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repo
3. Configure:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`

### Step 3: Set Environment Variables
```bash
CLINIKO_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=10000  # Render uses port 10000
```

### Step 4: Deploy
Click "Create Web Service" and wait for deployment.

## 🏗️ Option 4: AWS (For Enterprise)

### Using Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init
eb create production-env

# Set environment variables
eb setenv CLINIKO_API_KEY=your_api_key_here HOST=0.0.0.0 PORT=8000
```

### Using ECS with Fargate
1. Create ECR repository
2. Build and push Docker image
3. Create ECS cluster with Fargate
4. Configure load balancer and auto-scaling

## 🐧 Option 5: Digital Ocean App Platform

### Step 1: Create App Spec
```yaml
# .do/app.yaml
name: cliniko-mcp
services:
- name: web
  source_dir: cliniko_mcp_server
  github:
    repo: yourusername/yourrepo
    branch: main
  run_command: python main.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: CLINIKO_API_KEY
    value: "${cliniko_api_key}"
```

### Step 2: Deploy
1. Go to Digital Ocean App Platform
2. Create from GitHub
3. Use the app spec above

## 🔧 Option 6: Google Cloud Run

### Step 1: Build and Deploy
```bash
# Build Docker image
gcloud builds submit --tag gcr.io/PROJECT-ID/cliniko-mcp

# Deploy to Cloud Run
gcloud run deploy cliniko-mcp \
  --image gcr.io/PROJECT-ID/cliniko-mcp \
  --platform managed \
  --port 8000 \
  --set-env-vars CLINIKO_API_KEY=your_api_key_here \
  --allow-unauthenticated
```

## 🔒 Security Configuration

### Environment Variables (All Platforms)
```bash
CLINIKO_API_KEY=your_secure_api_key
HOST=0.0.0.0
PORT=8000  # or 10000 for some platforms
```

### HTTPS & SSL
- ✅ Railway: Automatic HTTPS
- ✅ Render: Automatic HTTPS
- ✅ AWS: Use ALB with SSL certificate
- ✅ Digital Ocean: Automatic HTTPS
- ✅ Google Cloud: Automatic HTTPS

### Network Security
- Use environment variables for secrets
- Never commit API keys to Git
- Enable health checks
- Configure proper CORS if needed

## 📊 Monitoring & Logging

### Health Checks
Your server includes a `/health` endpoint:
```bash
curl https://your-deployment-url/health
```

### Logs
- **Railway:** `railway logs`
- **Render:** Dashboard logs
- **AWS:** CloudWatch
- **Digital Ocean:** App logs
- **Google Cloud:** Cloud Logging

### Metrics
Monitor:
- Response times
- Error rates
- CPU/memory usage
- API call success rates

## 🎯 Eleven Labs Integration

### Step 1: Get Your Deployment URL
After deployment, you'll get a URL like:
- Railway: `https://cliniko-mcp-production.up.railway.app`
- Render: `https://cliniko-mcp.onrender.com`
- AWS: Your ALB URL

### Step 2: Configure Eleven Labs
In your Eleven Labs dashboard:
```json
{
  "mcp_server_url": "https://your-deployment-url",
  "mcp_server_port": 443,
  "tools": [
    "create_appointment",
    "list_appointments",
    "update_appointment",
    "delete_appointment",
    "create_patient",
    "list_patients",
    "update_patient",
    "delete_patient"
  ]
}
```

### Step 3: Test Integration
```bash
# Test MCP connection
curl https://your-deployment-url/health

# Test tool availability
curl -X POST https://your-deployment-url/tools/list_patients
```

## 🔄 Deployment Workflow

### For Updates
```bash
# Commit changes
git add .
git commit -m "Update MCP server"
git push origin main

# Platform-specific deployment
# Railway: Automatic
# Render: Automatic
# AWS: eb deploy
# Digital Ocean: Automatic
# Google Cloud: gcloud builds submit
```

### Rollback
- **Railway:** `railway rollback`
- **Render:** Use dashboard rollback
- **AWS:** `eb terminate` and redeploy
- **Others:** Revert git and redeploy

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plan | Best For |
|----------|-----------|-----------|----------|
| Railway | 512MB RAM, 1GB disk | $5/month | Beginners |
| Render | 750 hours/month | $7/month | Startups |
| Digital Ocean | Limited | $12/month | Developers |
| AWS | Free tier available | Variable | Enterprise |
| Google Cloud | Always free tier | Variable | Enterprise |

## 🚀 Quick Start (Railway Recommended)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up

# 3. Set environment variables
railway variables set CLINIKO_API_KEY=your_api_key_here

# 4. Get your URL
railway domain

# 5. Test
curl https://your-railway-url/health
```

## 📞 Support

### Common Issues
1. **Port conflicts:** Check if port 8000 is available
2. **API key errors:** Verify CLINIKO_API_KEY is set correctly
3. **Health check fails:** Ensure `/health` endpoint is accessible
4. **Eleven Labs connection:** Verify the MCP server URL is correct

### Getting Help
- Check deployment logs
- Verify environment variables
- Test with curl locally first
- Check Eleven Labs documentation

## 🎉 Success Checklist

- [ ] Server deployed and accessible
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Environment variables configured
- [ ] HTTPS enabled
- [ ] Eleven Labs connected successfully
- [ ] All tools responding correctly
- [ ] Monitoring and logging set up

**Your Cliniko MCP server is now production-ready and can be accessed by Eleven Labs from anywhere! 🚀**
