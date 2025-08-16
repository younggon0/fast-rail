# FastHTML + Railway Template

A ready-to-deploy hackathon template using FastHTML and Railway with integrated AI capabilities.

## Quick Start

1. **Setup Services:**
   ```bash
   cp .env.example .env
   # Edit .env with your service credentials:
   # - Supabase (database & auth)
   # - Neo4j (graph database)
   # - Anthropic (AI/LLM)
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

- `main.py` - Main application with auth, routes, and service dashboard
- `auth.py` - Authentication functions and session management
- `database.py` - Database helper class for Supabase operations
- `supabase_config.py` - Supabase client configuration
- `neo4j_config.py` - Neo4j client configuration and connection testing
- `llm.py` - LangChain integration with Anthropic Claude for AI features
- `setup_database.py` - Database setup script
- `.env.example` - Environment variables template (Supabase, Neo4j, Anthropic)
- `pyproject.toml` - Project dependencies (managed by uv)
- `nixpacks.toml` - Railway build configuration for uv
- `railway.toml` - Railway deployment configuration
- `runtime.txt` - Python runtime version

## Features

- 🚀 **One-click demo login** for hackathons
- 🔐 **Supabase authentication** (signup, login, logout)
- 📊 **Multi-database integration** with Supabase PostgreSQL + Neo4j graph database
- 🤖 **AI/LLM integration** with LangChain + Anthropic Claude
- 🎯 **Session management** with FastHTML
- ⚡ **Protected routes** with auth decorators
- 📈 **Service health monitoring** dashboard for all integrations
- 🔗 **Graph database ready** with Neo4j connection
- 🧠 **LLM capabilities** with structured chat and AI features
- 🛠️ **Development-friendly** with hot reload

## Development

Edit `main.py` to add your routes and features. The template includes:
- **Authentication system** ready to use with Supabase
- **Database operations** via `Database` class for PostgreSQL
- **Graph database** operations via Neo4j client
- **AI/LLM features** via LangChain and Anthropic integration
- **Session management** built-in with FastHTML
- **Service monitoring** dashboard showing connection status
- **Demo login** for easy testing

## Service Dashboard

Access `/dashboard` after login to see real-time status of:
- ✅ Supabase connection and authentication
- ✅ Neo4j graph database connection  
- ✅ LLM/Anthropic API connection

Happy hacking! 🚀