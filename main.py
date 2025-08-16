from fasthtml.common import *
import os

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required in production

# Import after loading environment variables
from auth import get_current_user, set_user_session, clear_user_session, sign_up_user, sign_in_user, sign_out_user
from database import Database

app, rt = fast_app()

@rt("/")
def get(session):
    user = get_current_user(session)
    if user:
        return Titled("FastHTML + Railway Template",
            Div(
                H1(f"Welcome back, {user.get('email', 'User')}!"),
                P("You are logged in to your FastHTML App"),
                A("Sign Out", href="/logout", style="margin: 10px;"),
                A("Dashboard", href="/dashboard", style="margin: 10px;"),
                style="text-align: center; margin-top: 50px;"
            )
        )
    else:
        return Titled("FastHTML + Railway Template",
            Div(
                H1("Welcome to your FastHTML App"),
                P("This is a template ready for hackathon development!"),
                P("Sign up or log in to get started."),
                Div(
                    A("🚀 Demo Login", href="/demo-login", style="margin: 10px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;"),
                    A("Sign Up", href="/signup", style="margin: 10px;"),
                    A("Log In", href="/login", style="margin: 10px;"),
                    style="margin: 20px 0;"
                ),
                style="text-align: center; margin-top: 50px;"
            )
        )

# Authentication routes
@rt("/demo-login")
def demo_login(session):
    """One-click demo login for hackathons"""
    # Create or login with demo user
    demo_email = "demo@hackathon.dev"
    demo_password = "demo123"
    
    # Try to sign in first, if fails then sign up
    result = sign_in_user(demo_email, demo_password)
    if not result["success"]:
        result = sign_up_user(demo_email, demo_password)
    
    if result["success"] and result["user"]:
        set_user_session(session, result["user"].dict())
    
    return RedirectResponse("/", status_code=302)

@rt("/signup")
def get_signup():
    return Titled("Sign Up",
        Div(
            H1("Create Account"),
            Form(
                Input(placeholder="Email", name="email", type="email", required=True),
                Input(placeholder="Password (min 6 chars)", name="password", type="password", required=True, minlength="6"),
                Button("Sign Up", type="submit"),
                method="post", action="/signup",
                style="display: flex; flex-direction: column; max-width: 300px; margin: 0 auto; gap: 10px;"
            ),
            Div(
                A("🚀 Quick Demo Login", href="/demo-login", style="margin: 10px; color: #007bff;"),
                Br(),
                A("Already have an account? Log In", href="/login"),
                style="margin-top: 20px;"
            ),
            style="text-align: center; margin-top: 50px;"
        )
    )

@rt("/signup", methods=["POST"])
def post_signup(session, email: str, password: str):
    result = sign_up_user(email, password)
    if result["success"]:
        if result["user"]:
            set_user_session(session, result["user"].dict())
        return RedirectResponse("/", status_code=302)
    else:
        return Titled("Sign Up Error",
            Div(
                H1("Sign Up Failed"),
                P(f"Error: {result['error']}"),
                A("Try Again", href="/signup"),
                style="text-align: center; margin-top: 50px;"
            )
        )

@rt("/login")
def get_login():
    return Titled("Log In",
        Div(
            H1("Log In"),
            Form(
                Input(placeholder="Email", name="email", type="email", required=True),
                Input(placeholder="Password", name="password", type="password", required=True),
                Button("Log In", type="submit"),
                method="post", action="/login",
                style="display: flex; flex-direction: column; max-width: 300px; margin: 0 auto; gap: 10px;"
            ),
            Div(
                A("🚀 Quick Demo Login", href="/demo-login", style="margin: 10px; color: #007bff;"),
                Br(),
                A("Don't have an account? Sign Up", href="/signup"),
                style="margin-top: 20px;"
            ),
            style="text-align: center; margin-top: 50px;"
        )
    )

@rt("/login", methods=["POST"])
def post_login(session, email: str, password: str):
    result = sign_in_user(email, password)
    if result["success"]:
        if result["user"]:
            set_user_session(session, result["user"].dict())
        return RedirectResponse("/", status_code=302)
    else:
        return Titled("Login Error",
            Div(
                H1("Login Failed"),
                P(f"Error: {result['error']}"),
                A("Try Again", href="/login"),
                style="text-align: center; margin-top: 50px;"
            )
        )

@rt("/logout")
def logout(session):
    clear_user_session(session)
    sign_out_user()
    return RedirectResponse("/", status_code=302)

@rt("/dashboard")
def dashboard(session):
    user = get_current_user(session)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    # Test database connections
    db_status = "❌ Not tested"
    try:
        # Simple connection test without requiring specific tables
        from supabase_config import init_supabase
        supabase = init_supabase()
        
        # Test basic connection (this will work even without custom tables)
        result = supabase.auth.get_user()
        db_status = "✅ Connected"
        
    except Exception as e:
        db_status = f"❌ Exception: {str(e)}"
    
    # Test Neo4j connection
    neo4j_status = "❌ Not tested"
    try:
        from neo4j_config import test_neo4j_connection
        neo4j_result = test_neo4j_connection()
        neo4j_status = neo4j_result["status"]
    except Exception as e:
        neo4j_status = f"❌ Exception: {str(e)}"
    
    return Titled("Dashboard",
        Div(
            H1("Dashboard"),
            P(f"Welcome to your dashboard, {user.get('email', 'User')}!"),
            P(f"Supabase Status: {db_status}"),
            P(f"Neo4j Status: {neo4j_status}"),
            P("This is where you can add your app's main functionality."),
            A("Home", href="/"),
            style="text-align: center; margin-top: 50px;"
        )
    )

@rt("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    serve()