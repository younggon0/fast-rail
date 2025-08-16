# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastHTML + Railway template designed for rapid hackathon development. The application uses FastHTML for web development with automatic HTML generation and built-in routing, integrated with Supabase for authentication and relational data, Neo4j for graph database capabilities, and LangChain with Anthropic for AI/LLM functionality, configured for seamless Railway deployment.

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

**Service Setup:**
```bash
cp .env.example .env       # Copy environment template
# Edit .env with service credentials:
# - Supabase (URL, keys)
# - Neo4j (URI, username, password)  
# - Anthropic (API key)
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

**Package Management:** Uses `uv` for fast dependency resolution. Dependencies defined in `pyproject.toml` with FastHTML, uvicorn, supabase-py, neo4j, langchain, langchain-anthropic, and python-dotenv as core requirements.

**Authentication & Database:** Multi-service architecture:
- **Supabase**: User authentication (signup, login, logout, sessions), PostgreSQL database with Row Level Security, real-time capabilities and file storage
- **Neo4j**: Graph database for relationships, recommendations, and advanced analytics
- **LLM Services**: LangChain integration with Anthropic Claude for AI-powered features
- Demo login for hackathon convenience (`demo@hackathon.dev`)
- Connection status monitoring for all services (Supabase, Neo4j, LLM)

## Key Patterns

- Route handlers return FastHTML components directly (no templates)
- Health check endpoint required for Railway deployment monitoring
- Development uses FastHTML's built-in hot reload via `serve()`
- Production uses uvicorn ASGI server with environment-based port binding
- Railway deployment uses `nixpacks.toml` for uv-based builds
- Multi-service integration with environment variable configuration
- Authentication middleware and session management
- Database helper classes for CRUD operations
- AI/LLM integration via LangChain framework
- Protected routes requiring authentication
- Service health monitoring on dashboard

## Service Modules

**Authentication (`auth.py`):** Supabase-based user management with signup, signin, signout, and session handling.

**Database (`database.py`):** PostgreSQL operations through Supabase client with CRUD helper methods.

**Neo4j (`neo4j_config.py`):** Graph database connection and testing utilities for relationship data.

**LLM (`llm.py`):** LangChain integration with Anthropic Claude for AI-powered features and chat capabilities.

**Main (`main.py`):** FastHTML application with routes, authentication flows, and service status dashboard.