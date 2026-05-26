from app.models.db import get_connection

class ModelEngineRepository:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM model_engines")
            return cursor.fetchall()
    
    @staticmethod
    def get_by_id(model_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM model_engines WHERE id = ?", (model_id,))
            return cursor.fetchone()
    
    @staticmethod
    def get_active():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM model_engines WHERE status = 'active'")
            return cursor.fetchall()
    
    @staticmethod
    def create(name, model_type, is_local, api_endpoint, api_key, token_limit, streaming):
        with get_connection() as conn:
            try:
                conn.execute("""
                    INSERT INTO model_engines (name, type, is_local, api_endpoint, api_key, token_limit, streaming) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, model_type, 1 if is_local else 0, api_endpoint, api_key, token_limit, 1 if streaming else 0))
                return True
            except:
                return False
    
    @staticmethod
    def update(model_id, name, model_type, is_local, api_endpoint, api_key, token_limit, streaming, status):
        with get_connection() as conn:
            conn.execute("""
                UPDATE model_engines 
                SET name=?, type=?, is_local=?, api_endpoint=?, api_key=?, token_limit=?, streaming=?, status=? 
                WHERE id=?
            """, (name, model_type, 1 if is_local else 0, api_endpoint, api_key, token_limit, 1 if streaming else 0, status, model_id))
            return True
    
    @staticmethod
    def delete(model_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM model_engines WHERE id=?", (model_id,))
            return True
