# FastHTML + Railway Template

A ready-to-deploy hackathon template using FastHTML and Railway.

## Quick Start

1. **Local Development:**
   ```bash
   uv sync
   source .venv/bin/activate
   python main.py
   ```
   Visit http://localhost:5001

2. **Deploy to Railway:**
   - Push to GitHub
   - Connect repository to Railway
   - Deploy automatically

## Project Structure

- `main.py` - Main application file
- `pyproject.toml` - Project dependencies (managed by uv)
- `Procfile` - Railway deployment command
- `railway.toml` - Railway configuration
- `runtime.txt` - Python runtime version

## Development

Edit `main.py` to add your routes and features. FastHTML provides:
- Automatic HTML generation
- Built-in routing
- Hot reload in development

Happy hacking! =�