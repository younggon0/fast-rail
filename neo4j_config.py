import os
from neo4j import GraphDatabase
from typing import Optional

# Global driver instance
neo4j_driver: Optional[GraphDatabase] = None

def get_neo4j_driver():
    """Initialize and return Neo4j driver"""
    uri = os.environ.get("NEO4J_URI")
    username = os.environ.get("NEO4J_USERNAME") 
    password = os.environ.get("NEO4J_PASSWORD")
    
    if not all([uri, username, password]):
        raise ValueError("NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD must be set in environment variables")
    
    return GraphDatabase.driver(uri, auth=(username, password))

def init_neo4j():
    """Initialize global Neo4j driver"""
    global neo4j_driver
    if neo4j_driver is None:
        neo4j_driver = get_neo4j_driver()
    return neo4j_driver

def test_neo4j_connection():
    """Test Neo4j connection and return status"""
    try:
        driver = init_neo4j()
        driver.verify_connectivity()
        return {"success": True, "status": "✅ Connected"}
    except ValueError as e:
        return {"success": False, "status": f"❌ Config Error: {str(e)}"}
    except Exception as e:
        return {"success": False, "status": f"❌ Connection Error: {str(e)}"}

def close_neo4j():
    """Close Neo4j driver connection"""
    global neo4j_driver
    if neo4j_driver:
        neo4j_driver.close()
        neo4j_driver = None