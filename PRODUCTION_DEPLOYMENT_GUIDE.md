# Production Deployment Guide - Cliniko MCP Server

## 🎯 Overview

This Cliniko MCP server has been **empirically tested and verified** for production use with Eleven Labs conversational AI. All API field formats have been validated through actual API calls.

## ✅ What's Been Verified

### API Field Formats
- ✅ All appointment creation fields tested and working
- ✅ All patient creation fields tested and working  
- ✅ ID formats validated (must be strings)
- ✅ Datetime formats validated (ISO with Z suffix)
- ✅ Default IDs extracted from working system

### Tool Reliability
- ✅ Input validation with helpful error messages
- ✅ Graceful error handling
- ✅ Success/failure indicators
- ✅ Working examples in tool descriptions

## 🚀 Deployment Steps

### 1. Environment Setup

**Requirements:**
```bash
Python 3.8+
pip install -r requirements.txt
```

**Environment Variables:**
```bash
# Required
CLINIKO_API_KEY=your_api_key_here

# Optional
PORT=8000
HOST=0.0.0.0
```

### 2. Docker Deployment (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  cliniko-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CLINIKO_API_KEY=${CLINIKO_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 3. Cloud Deployment Options

**Option A: Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Option B: Heroku**
```bash
# Create Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=$PORT" > Procfile

# Deploy
heroku create your-cliniko-mcp
heroku config:set CLINIKO_API_KEY=your_key
git push heroku main
```

**Option C: AWS Lambda**
```bash
# Use AWS SAM or Serverless Framework
pip install mangum
# Add Mangum wrapper to main.py
```

### 4. Eleven Labs Integration

**MCP Configuration:**
```json
{
  "server_url": "https://your-deployed-server.com",
  "tools": ["list_patients", "create_patient", "list_appointments", "create_appointment", "delete_appointment"]
}
```

**System Prompt:**
Use the content from `ELEVEN_LABS_SYSTEM_PROMPT.md`

## 🔒 Security Considerations

### API Key Security
- Store API key in environment variables
- Use secrets management in production
- Rotate keys regularly
- Monitor API usage

### Network Security
- Use HTTPS only in production
- Implement rate limiting
- Add authentication if needed
- Monitor for unusual activity

### Error Handling
- Don't expose internal errors to users
- Log errors for debugging
- Implement circuit breakers for API calls
- Handle Cliniko API rate limits

## 📊 Monitoring & Observability

### Health Checks
Add to `main.py`:
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log all MCP tool calls
logger.info(f"Tool called: {tool_name} with args: {args}")
```

### Metrics
- Track success/failure rates
- Monitor response times
- Alert on API errors
- Monitor memory/CPU usage

## 🧪 Testing in Production

### Smoke Tests
```python
# Test patient creation
test_patient = create_patient({
    "first_name": "Test",
    "last_name": "Patient" 
})

# Test appointment creation
test_appointment = create_appointment({
    "patient_id": test_patient["id"],
    "practitioner_id": "1752849161776013508",
    "appointment_type_id": "1752849165005627509", 
    "business_id": "1752849165332784051",
    "appointment_start": "2025-12-01T10:00:00Z",
    "appointment_end": "2025-12-01T11:00:00Z"
})
```

### Integration Tests
- Test full booking workflow
- Test error scenarios
- Test edge cases (invalid dates, etc.)
- Test with actual Eleven Labs agent

## 🔧 Troubleshooting

### Common Issues

**1. API Key Issues**
```
Error: Client error '401 Unauthorized'
Solution: Check CLINIKO_API_KEY environment variable
```

**2. Field Format Errors**
```
Error: Client error '422 Unprocessable Entity'
Solution: Use exact field names from verified examples
```

**3. ID Format Issues**
```
Error: Invalid patient_id format
Solution: Ensure IDs are strings, not integers
```

**4. Datetime Format Issues**
```
Error: Invalid appointment_start format
Solution: Use ISO format with Z suffix (2025-09-05T10:00:00Z)
```

### Debug Mode
Add to environment:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📋 Production Checklist

- [ ] Environment variables set
- [ ] API key tested
- [ ] Health check endpoint working
- [ ] Error handling tested
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Security review completed
- [ ] Eleven Labs integration tested
- [ ] Backup/recovery plan in place
- [ ] Documentation updated

## 🎯 Performance Optimization

### Caching
- Cache patient lookups
- Cache practitioner/business IDs
- Implement Redis for session storage

### Rate Limiting
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.tool("create_appointment")
@limiter.limit("10/minute")
async def create_appointment(...):
```

### Connection Pooling
```python
# Use connection pooling for HTTP clients
import httpx
client = httpx.AsyncClient(limits=httpx.Limits(max_connections=10))
```

## 📈 Scaling Considerations

- Use horizontal scaling for high traffic
- Implement queue for async processing
- Consider database for caching
- Monitor API rate limits
- Use CDN for static assets

## 🔄 Maintenance

### Regular Tasks
- Monitor API usage
- Update dependencies
- Review logs for errors
- Test integrations
- Backup configurations

### Updates
- Test changes in staging first
- Use blue-green deployments
- Monitor after deployments
- Have rollback plan ready

---

**Final Note:** This deployment guide is based on empirically tested configurations. All field formats and API calls have been verified to work correctly with the actual Cliniko API.
