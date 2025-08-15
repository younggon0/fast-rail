import os
from supabase import create_client, Client
from typing import Optional

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    return create_client(url, key)

# Global client instance
supabase: Optional[Client] = None

def init_supabase():
    """Initialize global Supabase client"""
    global supabase
    if supabase is None:
        supabase = get_supabase_client()
    return supabase