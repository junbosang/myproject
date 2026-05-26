from app.models.db import get_connection

class DigitalEmployeeRepository:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM digital_employees")
            return cursor.fetchall()
    
    @staticmethod
    def get_by_id(emp_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM digital_employees WHERE id = ?", (emp_id,))
            return cursor.fetchone()
    
    @staticmethod
    def get_by_type(emp_type):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM digital_employees WHERE type = ?", (emp_type,))
            return cursor.fetchall()
    
    @staticmethod
    def create(name, emp_type, description, avatar, prompt):
        with get_connection() as conn:
            try:
                conn.execute("""
                    INSERT INTO digital_employees (name, type, description, avatar, prompt) 
                    VALUES (?, ?, ?, ?, ?)
                """, (name, emp_type, description, avatar, prompt))
                return True
            except:
                return False
    
    @staticmethod
    def update(emp_id, name, emp_type, description, avatar, prompt, status):
        with get_connection() as conn:
            conn.execute("""
                UPDATE digital_employees 
                SET name=?, type=?, description=?, avatar=?, prompt=?, status=? 
                WHERE id=?
            """, (name, emp_type, description, avatar, prompt, status, emp_id))
            return True
    
    @staticmethod
    def delete(emp_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM digital_employees WHERE id=?", (emp_id,))
            return True
