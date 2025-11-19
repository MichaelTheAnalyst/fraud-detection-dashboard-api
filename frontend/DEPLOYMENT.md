# Deployment Guide - Fraud Detection Dashboard Frontend

## 🚀 Quick Deploy to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub
2. Click **"Add New..."** → **"Project"**
3. Import your `fraud-detection-dashboard-api` repository
4. Configure the project:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `dist` (auto-detected)
   - **Environment Variable:**
     - Key: `VITE_API_URL`
     - Value: `https://fraud-detection-dashboard-api.onrender.com`
5. Click **"Deploy"**

Your dashboard will be live in ~2 minutes! 🎉

### Option 2: Deploy via Vercel CLI

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

When prompted:
- Set root directory: `frontend`
- Add environment variable: `VITE_API_URL=https://fraud-detection-dashboard-api.onrender.com`

---

## 🌐 Alternative: Deploy to Netlify

1. Go to [netlify.com](https://netlify.com) and sign in with GitHub
2. Click **"Add new site"** → **"Import an existing project"**
3. Select your repository
4. Configure:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`
   - **Environment variables:**
     - `VITE_API_URL` = `https://fraud-detection-dashboard-api.onrender.com`
5. Deploy

---

## 🔧 Local Development

To test locally with the production API:

```bash
cd frontend
npm install
npm run dev
```

The app will automatically use the production API URL when built for production.

---

## 📝 Environment Variables

The app uses `VITE_API_URL` environment variable:
- **Production:** `https://fraud-detection-dashboard-api.onrender.com`
- **Local Development:** `http://localhost:8000` (default)

---

## ✅ After Deployment

Once deployed, you'll get a URL like:
- `https://fraud-dashboard.vercel.app` (Vercel)
- `https://fraud-dashboard.netlify.app` (Netlify)

Share this URL and I'll update your portfolio! 🚀

