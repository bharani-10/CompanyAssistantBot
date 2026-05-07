# Streamlit Deployment Guide

## Overview
This guide covers deploying the SWS AI Company Assistant to Streamlit Cloud or other hosting platforms.

## Prerequisites
- Python 3.8+
- All dependencies from `requirements.txt`
- API keys for LLM (Gemini or OpenAI)
- PDF documents in the project directory

## Local Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-pro
LLM_PROVIDER=gemini
TEMPERATURE=0.7
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000
PDF_DIRECTORY=.
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### 3. Run Backend (FastAPI)
In one terminal:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Run Frontend (Streamlit)
In another terminal:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Deployment to Streamlit Cloud

### 1. Prepare Repository
```bash
git add .
git commit -m "Prepare for Streamlit deployment"
git push origin main
```

### 2. Create Streamlit Account
- Go to https://streamlit.io/cloud
- Sign up with GitHub account
- Authorize Streamlit to access your repositories

### 3. Deploy App
1. Click "New app"
2. Select your repository
3. Select branch: `main`
4. Set main file path: `app.py`
5. Click "Deploy"

### 4. Configure Secrets
In Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Secrets"
3. Add your environment variables:
```
GEMINI_API_KEY = "your_gemini_api_key_here"
LLM_MODEL = "gemini-pro"
LLM_PROVIDER = "gemini"
TEMPERATURE = "0.7"
API_URL = "http://your-backend-url:8000"
PDF_DIRECTORY = "."
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
```

### 5. Deploy Backend
The backend (FastAPI) needs to be deployed separately. Options:

#### Option A: Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Deploy
git push heroku main

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key
heroku config:set LLM_MODEL=gemini-pro
heroku config:set LLM_PROVIDER=gemini
```

#### Option B: Railway
1. Go to https://railway.app
2. Connect GitHub repository
3. Add environment variables
4. Deploy

#### Option C: Render
1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy

### 6. Update Streamlit Secrets
After deploying backend, update the `API_URL` in Streamlit Cloud secrets to point to your deployed backend.

## Docker Deployment

### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 8000

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Build and Run
```bash
docker build -t sws-ai-assistant .
docker run -p 8501:8501 -p 8000:8000 --env-file .env sws-ai-assistant
```

## Troubleshooting

### API Connection Issues
- Ensure backend is running and accessible
- Check `API_URL` in environment variables
- Verify firewall/network settings
- Check logs: `streamlit run app.py --logger.level=debug`

### PDF Loading Issues
- Ensure PDF files are in the correct directory
- Check file permissions
- Verify PDF format compatibility
- Check `PDF_DIRECTORY` setting

### Memory Issues
- Reduce `CHUNK_SIZE` in config
- Reduce `RETRIEVAL_K` (number of chunks to retrieve)
- Use smaller embedding model

### API Key Issues
- Verify API key is correct
- Check API key has necessary permissions
- Ensure API key is not expired
- For Gemini: https://makersuite.google.com/app/apikey
- For OpenAI: https://platform.openai.com/api-keys

## Performance Optimization

### 1. Caching
- Streamlit automatically caches function results
- Use `@st.cache_data` for expensive operations
- Use `@st.cache_resource` for resources like API connections

### 2. Vector Store
- Pre-build and persist vector store
- Use smaller embedding models for faster inference
- Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP`

### 3. LLM
- Use faster models (e.g., gpt-3.5-turbo instead of gpt-4)
- Reduce `MAX_TOKENS`
- Adjust `TEMPERATURE` for faster responses

## Monitoring

### Logs
- Streamlit: Check browser console and terminal
- FastAPI: Check terminal output
- Streamlit Cloud: Check app logs in dashboard

### Metrics
- Response time
- API availability
- Error rates
- User engagement

## Security Best Practices

1. **Never commit secrets**
   - Use `.env` files (add to `.gitignore`)
   - Use Streamlit Secrets in cloud deployment

2. **API Key Management**
   - Rotate keys regularly
   - Use environment-specific keys
   - Monitor key usage

3. **CORS Configuration**
   - Restrict origins in production
   - Update `CORS_ORIGINS` in config

4. **Rate Limiting**
   - Enable rate limiting in FastAPI
   - Monitor for abuse

5. **Data Privacy**
   - Ensure PDFs don't contain sensitive data
   - Implement access controls if needed
   - Review conversation logs

## Maintenance

### Regular Tasks
- Monitor API health
- Check error logs
- Update dependencies
- Backup vector store
- Review performance metrics

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Rebuild vector store if needed
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline(rebuild=True)"
```

## Support

For issues or questions:
1. Check logs for error messages
2. Review this guide
3. Check Streamlit documentation: https://docs.streamlit.io
4. Check LangChain documentation: https://python.langchain.com
