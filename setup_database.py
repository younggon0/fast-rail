#!/usr/bin/env python3
"""
Database setup script for FastHTML + Supabase app
Run this after setting up your Supabase project to create required tables.
"""

import os
from supabase_config import init_supabase

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def setup_database():
    """Display SQL to run manually in Supabase dashboard"""
    
    sql_script = """
-- User sessions tracking table
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    email TEXT,
    login_time TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own sessions
CREATE POLICY IF NOT EXISTS "Users can view own sessions" ON user_sessions
    FOR SELECT USING (auth.uid() = user_id);

-- Policy: Users can insert their own sessions
CREATE POLICY IF NOT EXISTS "Users can insert own sessions" ON user_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Example app data table
CREATE TABLE IF NOT EXISTS app_data (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Enable RLS on app_data
ALTER TABLE app_data ENABLE ROW LEVEL SECURITY;

-- Policy: Users can manage their own data
CREATE POLICY IF NOT EXISTS "Users can manage own data" ON app_data
    FOR ALL USING (auth.uid() = user_id);
"""
    
    print("🚀 Database Setup SQL")
    print("=" * 50)
    print("\n📋 Copy and paste this SQL into your Supabase dashboard:")
    print("1. Go to https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Click 'SQL Editor' in the sidebar")
    print("4. Paste and run this SQL:\n")
    
    print(sql_script)
    
    print("=" * 50)
    print("✅ After running the SQL, your database will have:")
    print("- user_sessions: Track user login sessions")
    print("- app_data: Example table for your app data")
    print("- Row Level Security: Users only see their own data")
    
    return True

def test_connection():
    """Test database connection"""
    try:
        supabase = init_supabase()
        
        # Test basic connection by checking auth users table
        result = supabase.auth.get_user()
        print("✅ Supabase connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("\nCheck your environment variables:")
        print("- SUPABASE_URL")
        print("- SUPABASE_KEY")
        return False

if __name__ == "__main__":
    print("FastHTML + Supabase Database Setup")
    print("=" * 40)
    
    # Always show setup instructions
    setup_database()
    
    print("\n" + "=" * 40)
    print("Connection Test:")
    if test_connection():
        print("✅ Ready to use database operations!")
    else:
        print("💡 Tip: Make sure you've:")
        print("1. Created a Supabase project at https://supabase.com")
        print("2. Copied .env.example to .env")
        print("3. Added your Supabase URL and API key to .env")