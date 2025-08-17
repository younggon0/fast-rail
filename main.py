from fasthtml.common import *
import os
import json

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from gmail_client import GmailClient
from email_clusterer import EmailClusterer

app, rt = fast_app()

gmail_clients = {}

@rt("/")
def get(session):
    return Titled("Email Cluster Manager",
        Div(
            H1("📧 Email Cluster Manager"),
            P("Organize your last 200 emails into actionable groups"),
            Div(
                H2("Connect to Gmail"),
                P("You'll need an App Password from Google:"),
                Ol(
                    Li("Go to ", A("Google Account Settings", href="https://myaccount.google.com/apppasswords", target="_blank")),
                    Li("Enable 2-factor authentication if not already enabled"),
                    Li("Generate an App Password for 'Mail'"),
                    Li("Use that password below (not your regular Gmail password)")
                ),
                Form(
                    Input(placeholder="Gmail address", name="email", type="email", required=True, style="width: 300px; padding: 10px; margin: 5px;"),
                    Input(placeholder="App Password", name="password", type="password", required=True, style="width: 300px; padding: 10px; margin: 5px;"),
                    Button("Connect & Analyze Emails", type="submit", style="padding: 10px 20px; background: #4285f4; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;"),
                    method="post", action="/connect",
                    style="display: flex; flex-direction: column; align-items: center; margin: 20px 0;"
                ),
                style="background: #f8f9fa; padding: 30px; border-radius: 10px; margin: 20px auto; max-width: 600px;"
            ),
            style="text-align: center; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;"
        )
    )

@rt("/connect", methods=["POST"])
def connect_gmail(session, email: str, password: str):
    client = GmailClient(email, password)
    result = client.connect()
    
    if not result["success"]:
        return Titled("Connection Error",
            Div(
                H1("❌ Connection Failed"),
                P(f"Error: {result.get('error', 'Unknown error')}"),
                P("Make sure you're using an App Password, not your regular Gmail password"),
                A("Try Again", href="/", style="color: #4285f4;"),
                style="text-align: center; margin-top: 50px; padding: 20px;"
            )
        )
    
    session_id = f"{email}_{id(session)}"
    gmail_clients[session_id] = client
    session['gmail_session'] = session_id
    
    return RedirectResponse("/analyze", status_code=302)

@rt("/analyze")
def analyze_emails(session):
    session_id = session.get('gmail_session')
    if not session_id or session_id not in gmail_clients:
        return RedirectResponse("/", status_code=302)
    
    client = gmail_clients[session_id]
    
    return Titled("Analyzing Emails",
        Div(
            H1("⏳ Analyzing Your Emails..."),
            P("Fetching and clustering your last 200 emails. This may take a moment..."),
            Div(
                style="width: 100%; height: 4px; background: #e0e0e0; border-radius: 2px; overflow: hidden;",
                children=[
                    Div(style="width: 100%; height: 100%; background: #4285f4; animation: loading 2s ease-in-out infinite;")
                ]
            ),
            Script("""
                setTimeout(() => {
                    window.location.href = '/clusters';
                }, 2000);
            """),
            Style("""
                @keyframes loading {
                    0% { transform: translateX(-100%); }
                    50% { transform: translateX(0); }
                    100% { transform: translateX(100%); }
                }
            """),
            style="text-align: center; margin-top: 100px; padding: 20px;"
        )
    )

@rt("/clusters")
def show_clusters(session):
    session_id = session.get('gmail_session')
    if not session_id or session_id not in gmail_clients:
        return RedirectResponse("/", status_code=302)
    
    client = gmail_clients[session_id]
    
    emails = client.fetch_recent_emails(200)
    
    if not emails:
        return Titled("No Emails",
            Div(
                H1("📭 No Emails Found"),
                P("Could not fetch emails from your inbox"),
                A("Try Again", href="/", style="color: #4285f4;"),
                style="text-align: center; margin-top: 50px;"
            )
        )
    
    clusterer = EmailClusterer()
    clusters = clusterer.cluster_emails(emails)
    
    session['clusters'] = json.dumps(clusters, default=str)
    
    cluster_divs = []
    for i, cluster in enumerate(clusters):
        priority_color = {
            "high": "#dc3545",
            "medium": "#ffc107", 
            "low": "#28a745"
        }.get(cluster.get("priority", "medium"), "#6c757d")
        
        email_list = []
        for email in cluster.get("emails", [])[:5]:
            email_list.append(
                Div(
                    P(Strong(email.get("from", "Unknown")[:40]), style="margin: 0; font-size: 12px;"),
                    P(email.get("subject", "No subject")[:60], style="margin: 0; font-size: 11px; color: #666;"),
                    style="padding: 8px; border-bottom: 1px solid #eee;"
                )
            )
        
        if cluster.get("count", 0) > 5:
            email_list.append(
                P(f"... and {cluster.get('count', 0) - 5} more emails", 
                  style="padding: 8px; font-style: italic; color: #666; font-size: 11px;")
            )
        
        cluster_divs.append(
            Div(
                Div(
                    H3(cluster.get("name", "Unnamed Cluster"), style="margin: 0 0 10px 0;"),
                    Span(f"Priority: {cluster.get('priority', 'medium').upper()}", 
                         style=f"background: {priority_color}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;"),
                    Span(f" {cluster.get('count', 0)} emails", style="margin-left: 10px; color: #666;"),
                    style="margin-bottom: 10px;"
                ),
                P(cluster.get("description", "No description"), style="color: #333; margin: 10px 0;"),
                Div(*email_list, style="background: #f8f9fa; border-radius: 5px; margin: 10px 0; max-height: 300px; overflow-y: auto;"),
                Form(
                    Input(type="hidden", name="cluster_index", value=str(i)),
                    Button(f"📁 Archive All {cluster.get('count', 0)} Emails", 
                           type="submit",
                           style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer; width: 100%;"),
                    method="post", action="/archive"
                ),
                style="background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
            )
        )
    
    return Titled("Email Clusters",
        Div(
            H1("📊 Your Email Clusters"),
            P(f"Analyzed {len(emails)} emails and grouped them into {len(clusters)} actionable clusters"),
            Div(
                *cluster_divs,
                style="max-width: 800px; margin: 0 auto;"
            ),
            Div(
                A("← Analyze Again", href="/", style="color: #4285f4; margin: 20px;"),
                style="text-align: center; margin: 40px 0;"
            ),
            style="padding: 20px; background: #f5f5f5; min-height: 100vh;"
        )
    )

@rt("/archive", methods=["POST"])
def archive_cluster(session, cluster_index: str):
    session_id = session.get('gmail_session')
    if not session_id or session_id not in gmail_clients:
        return RedirectResponse("/", status_code=302)
    
    client = gmail_clients[session_id]
    clusters_json = session.get('clusters', '[]')
    clusters = json.loads(clusters_json)
    
    try:
        cluster_idx = int(cluster_index)
        if 0 <= cluster_idx < len(clusters):
            cluster = clusters[cluster_idx]
            email_ids = [email.get("id") for email in cluster.get("emails", [])]
            
            result = client.archive_emails(email_ids)
            
            if result["success"]:
                return Titled("Success",
                    Div(
                        H1("✅ Emails Archived!"),
                        P(f"Successfully archived {result.get('archived', 0)} emails from '{cluster.get('name', 'cluster')}'"),
                        A("← Back to Clusters", href="/clusters", style="color: #4285f4;"),
                        style="text-align: center; margin-top: 50px; padding: 20px;"
                    )
                )
            else:
                return Titled("Error",
                    Div(
                        H1("❌ Archive Failed"),
                        P(f"Error: {result.get('error', 'Unknown error')}"),
                        A("← Back to Clusters", href="/clusters", style="color: #4285f4;"),
                        style="text-align: center; margin-top: 50px; padding: 20px;"
                    )
                )
    except Exception as e:
        return Titled("Error",
            Div(
                H1("❌ Error"),
                P(f"Error processing request: {str(e)}"),
                A("← Back to Clusters", href="/clusters", style="color: #4285f4;"),
                style="text-align: center; margin-top: 50px; padding: 20px;"
            )
        )
    
    return RedirectResponse("/clusters", status_code=302)

@rt("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    serve()