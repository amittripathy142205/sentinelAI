# 🔧 Frontend Pages Fix - Install Guide

## Problem
The error shows: `Failed to resolve import "./pages/Dashboard" from "src/App.jsx"`

This means the page files are either missing or corrupted.

---

## ✅ SOLUTION (2 Minutes)

### **Step 1: Download All Page Files**

I've created all 6 missing page components:
- ✅ Dashboard.jsx
- ✅ LiveMonitor.jsx
- ✅ Evidence.jsx
- ✅ Reports.jsx
- ✅ LocationMap.jsx
- ✅ Analytics.jsx

---

### **Step 2: Copy Files to Your Project**

Copy all 6 files to:
```
C:\Users\asus\Downloads\smartsentinel\smartsentinel\frontend\src\pages\
```

**IMPORTANT:** Make sure they go into the `pages` folder!

---

### **Step 3: Restart Frontend**

```cmd
cd C:\Users\asus\Downloads\smartsentinel\smartsentinel\frontend
npm run dev
```

---

## 📋 File Checklist

After copying, your `frontend/src/pages/` folder should have these 9 files:

```
frontend/src/pages/
├── LandingPage.jsx     ✓
├── LoginPage.jsx       ✓
├── RegisterPage.jsx    ✓
├── Dashboard.jsx       ← Copy this
├── LiveMonitor.jsx     ← Copy this
├── Evidence.jsx        ← Copy this
├── Reports.jsx         ← Copy this
├── LocationMap.jsx     ← Copy this
└── Analytics.jsx       ← Copy this
```

---

## 🎯 Verify It Works

After copying files and running `npm run dev`, you should see:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

**No more import errors!**

---

## 🐛 If Still Having Issues

### Problem: "Cannot find module"
**Solution:** Make sure files have the exact names (case-sensitive):
- ✅ `Dashboard.jsx` (not `dashboard.jsx`)
- ✅ File extension is `.jsx` (not `.js`)

### Problem: "Files are there but still error"
**Solution:** Clean restart
```cmd
cd frontend
rmdir /s /q node_modules .vite
del package-lock.json
npm install
npm run dev
```

---

## 💡 Quick Copy Method

**Windows Quick Copy:**
1. Select all 6 files
2. Right-click → Copy
3. Navigate to `C:\Users\asus\Downloads\smartsentinel\smartsentinel\frontend\src\pages\`
4. Right-click → Paste
5. Overwrite if asked

---

## ✅ Success Check

Browser should open to `http://localhost:5173` and show:
- Landing page loads
- Can click Login
- No console errors about missing imports

---

**Just copy those 6 files and restart! That's it! 🚀**
