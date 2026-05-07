# Quick Deployment Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# Get it from: https://makersuite.google.com/app/apikey
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Backend (Terminal 1)
```bash
python main.py
```
Backend will be available at: `http://localhost:8000`

### Step 4: Run Frontend (Terminal 2)
```bash
streamlit run app.py
```
Frontend will be available at: `http://localhost:8501`

### Step 5: Test
- Open http://localhost:8501 in your browser
- Ask a question about company policies
- You should get an answer from the documents

---

## 🐳 Docker Deployment (One Command)

```bash
# Make sure .env is configured with your API key
docker-compose up
```

Then visit: http://localhost:8501

---

## ☁️ Deploy to Streamlit Cloud

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud
- Go to https://streamlit.io/cloud
- Click "New app"
- Select your repository
- Set main file: `app.py`
- Click "Deploy"

### 3. Add Secrets
In Streamlit Cloud dashboard:
1. Go to app settings
2. Click "Secrets"
3. Add:
```
GEMINI_API_KEY = "your_key_here"
LLM_MODEL = "gemini-pro"
LLM_PROVIDER = "gemini"
API_URL = "http://your-backend-url:8000"
```

---

## 🌐 Deploy Backend to Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key
heroku config:set LLM_MODEL=gemini-pro
heroku config:set LLM_PROVIDER=gemini

# View logs
heroku logs --tail
```

Backend URL: `https://your-app-name.herokuapp.com`

---

## 📋 Deployment Checklist

- [ ] `.env` file created with API key
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Backend running: `python main.py`
- [ ] Frontend running: `streamlit run app.py`
- [ ] Can access http://localhost:8501
- [ ] Can ask questions and get answers
- [ ] Ready to deploy to cloud

---

## 🔑 Getting API Keys

### Google Gemini (Recommended - Free!)
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to `.env`: `GEMINI_API_KEY=your_key`

### OpenAI (Optional)
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Add to `.env`: `OPENAI_API_KEY=your_key`

---

## ✅ Verify Installation

```bash
python quick_verify.py
```

Should show all [OK] status

---

## 🆘 Common Issues

### "Cannot connect to API"
- Make sure backend is running: `python main.py`
- Check API_URL in .env

### "No PDF files found"
- Ensure PDF files are in the project directory
- Check file permissions

### "API key not valid"
- Verify key is correct
- Check key hasn't expired
- Ensure key has necessary permissions

### "Out of memory"
- Reduce CHUNK_SIZE in config.py
- Reduce RETRIEVAL_K value
- Use smaller embedding model

---

## 📞 Need Help?

1. Check DEPLOYMENT_GUIDE.md for detailed instructions
2. Check DEPLOYMENT_SUMMARY.md for status
3. Review logs for error messages
4. Check documentation links in DEPLOYMENT_GUIDE.md

---

**Ready to deploy? Start with Step 1 above!**
