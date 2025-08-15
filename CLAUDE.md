# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastHTML + Railway template designed for rapid hackathon development. The application uses FastHTML for web development with automatic HTML generation and built-in routing, integrated with Supabase for authentication and database operations, configured for seamless Railway deployment.

## Development Commands

**Local Development:**
```bash
uv sync                    # Install/sync dependencies
source .venv/bin/activate  # Activate virtual environment  
python main.py             # Start development server (http://localhost:5001)
```

**Dependency Management:**
```bash
uv add <package>           # Add new dependency
uv remove <package>        # Remove dependency
```

**Supabase Setup:**
```bash
cp .env.example .env       # Copy environment template
# Edit .env with Supabase credentials
uv run python setup_database.py  # Get SQL for database setup
```

**Railway Deployment:**
```bash
railway login              # Login to Railway
railway init               # Create new project
railway up                 # Deploy application
railway open               # Open deployed app
railway status             # Check deployment status
```

## Architecture

**Core Application:** Single-file FastHTML app (`main.py`) using the `fast_app()` pattern with route decorators (`@rt`). Routes return FastHTML components (Titled, Div, H1, P) for automatic HTML generation.

**Deployment Configuration:** 
- `nixpacks.toml` - Railway build configuration for uv package manager
- `railway.toml` - Railway-specific config with health check endpoint (`/health`)
- `runtime.txt` - Python version specification for deployment

**Package Management:** Uses `uv` for fast dependency resolution. Dependencies defined in `pyproject.toml` with FastHTML, uvicorn, supabase-py, and python-dotenv as core requirements.

**Authentication & Database:** Integrated Supabase backend providing:
- User authentication (signup, login, logout, sessions)
- PostgreSQL database with Row Level Security
- Real-time capabilities and file storage
- Demo login for hackathon convenience (`demo@hackathon.dev`)

## Key Patterns

- Route handlers return FastHTML components directly (no templates)
- Health check endpoint required for Railway deployment monitoring
- Development uses FastHTML's built-in hot reload via `serve()`
- Production uses uvicorn ASGI server with environment-based port binding
- Railway deployment uses `nixpacks.toml` for uv-based builds
- Supabase integration with environment variable configuration
- Authentication middleware and session management
- Database helper class for CRUD operations
- Protected routes requiring authentication