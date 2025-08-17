# 📧 Email Cluster Manager

A FastHTML app that clusters your last 200 Gmail emails into actionable groups using AI, with one-click archive functionality.

## 🚀 Quick Start (15 minutes)

### 1. Set up your Anthropic API Key
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

Get your API key from: https://console.anthropic.com/settings/keys

### 2. Get a Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-factor authentication if not already enabled
3. Generate an App Password for "Mail"
4. Save this password (you'll enter it in the app)

### 3. Install and Run
```bash
uv sync
uv run python main.py
```

Open http://localhost:5001

### 4. Use the App
1. Enter your Gmail address and App Password
2. Wait for the app to fetch and analyze your emails
3. Review the clusters (organized by action needed)
4. Click "Archive All" to archive an entire cluster

## 📊 Features

- **Smart Clustering**: Uses Claude to group emails by required action
- **Priority Levels**: High/Medium/Low priority indicators
- **Email Previews**: Shows first 5 emails in each cluster
- **One-Click Archive**: Archive entire clusters instantly
- **Actionable Groups**: Examples:
  - "Newsletters to Unsubscribe"
  - "Meeting Requests to Schedule"
  - "Bills to Pay"
  - "Support Tickets to Address"

## 🏗️ Architecture

```
main.py              - FastHTML web app with routes
gmail_client.py      - IMAP connection and email operations
email_clusterer.py   - AI-powered email clustering logic
```

## 🚢 Deploy to Railway

```bash
railway login
railway init
railway up
```

Add your ANTHROPIC_API_KEY in Railway dashboard under Variables.

## ⚡ Performance

- Fetches last 200 emails
- Clusters in ~5-10 seconds
- Archives instantly via IMAP

## 🔒 Security Notes

- Uses Gmail App Passwords (not your main password)
- No emails are stored permanently
- Session-based authentication
- All operations happen in real-time

## 📝 Customization

Edit `email_clusterer.py` to customize:
- Number of clusters (default: 3-5)
- Clustering criteria
- Priority assignments
- Action suggestions