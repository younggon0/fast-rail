# FastHTML + Railway Template

A ready-to-deploy hackathon template using FastHTML and Railway.

## Quick Start

1. **Setup Supabase:**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   uv run python setup_database.py  # Get SQL to run in Supabase dashboard
   ```

2. **Local Development:**
   ```bash
   uv sync
   source .venv/bin/activate
   python main.py
   ```
   Visit http://localhost:5001

3. **Deploy to Railway:**
   ```bash
   railway login
   railway init    # Or railway link for existing projects
   railway up      # Deploy
   railway open    # View deployed app
   ```
   Or connect GitHub repository to Railway dashboard for auto-deploy

## Project Structure

- `main.py` - Main application with auth and routes
- `auth.py` - Authentication functions and session management
- `database.py` - Database helper class for Supabase operations
- `supabase_config.py` - Supabase client configuration
- `setup_database.py` - Database setup script
- `.env.example` - Environment variables template
- `pyproject.toml` - Project dependencies (managed by uv)
- `nixpacks.toml` - Railway build configuration for uv
- `railway.toml` - Railway deployment configuration
- `runtime.txt` - Python runtime version

## Features

- 🚀 **One-click demo login** for hackathons
- 🔐 **Supabase authentication** (signup, login, logout)
- 📊 **Database integration** with helper functions
- 🎯 **Session management** with FastHTML
- ⚡ **Protected routes** with auth decorators
- 🛠️ **Development-friendly** with hot reload

## Development

Edit `main.py` to add your routes and features. The template includes:
- Authentication system ready to use
- Database operations via `Database` class
- Session management built-in
- Demo login for easy testing

Happy hacking! =�