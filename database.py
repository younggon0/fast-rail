from supabase_config import init_supabase
from typing import List, Dict, Any, Optional

# Initialize Supabase
supabase = init_supabase()

class Database:
    """Database helper class for Supabase operations"""
    
    @staticmethod
    def insert(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert data into a table"""
        try:
            response = supabase.table(table).insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def select(table: str, columns: str = "*", filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Select data from a table with optional filters"""
        try:
            query = supabase.table(table).select(columns)
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def update(table: str, data: Dict[str, Any], filters: Dict[str, Any]) -> Dict[str, Any]:
        """Update data in a table"""
        try:
            query = supabase.table(table).update(data)
            
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete(table: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Delete data from a table"""
        try:
            query = supabase.table(table)
            
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.delete().execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def upsert(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert or update data in a table"""
        try:
            response = supabase.table(table).upsert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}