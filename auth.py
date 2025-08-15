from fasthtml.common import *
from supabase_config import init_supabase
from typing import Optional, Dict, Any
import json

# Initialize Supabase
supabase = init_supabase()

def get_current_user(session) -> Optional[Dict[str, Any]]:
    """Get current authenticated user from session"""
    user_data = session.get('user')
    if user_data:
        return json.loads(user_data) if isinstance(user_data, str) else user_data
    return None

def set_user_session(session, user_data: Dict[str, Any]):
    """Store user data in session"""
    # Extract only JSON-serializable fields
    safe_user_data = {
        'id': user_data.get('id'),
        'email': user_data.get('email'),
        'created_at': user_data.get('created_at').isoformat() if user_data.get('created_at') else None,
        'last_sign_in_at': user_data.get('last_sign_in_at').isoformat() if user_data.get('last_sign_in_at') else None
    }
    session['user'] = json.dumps(safe_user_data)

def clear_user_session(session):
    """Clear user session"""
    session.pop('user', None)

def auth_required(func):
    """Decorator to require authentication for routes"""
    def wrapper(*args, **kwargs):
        session = kwargs.get('session') or args[0] if args else None
        if not session or not get_current_user(session):
            return RedirectResponse("/login", status_code=302)
        return func(*args, **kwargs)
    return wrapper

def sign_up_user(email: str, password: str) -> Dict[str, Any]:
    """Sign up a new user"""
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return {"success": True, "user": response.user, "session": response.session}
    except Exception as e:
        return {"success": False, "error": str(e)}

def sign_in_user(email: str, password: str) -> Dict[str, Any]:
    """Sign in an existing user"""
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"success": True, "user": response.user, "session": response.session}
    except Exception as e:
        return {"success": False, "error": str(e)}

def sign_out_user() -> Dict[str, Any]:
    """Sign out current user"""
    try:
        supabase.auth.sign_out()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}