from app.models.db import get_connection
from app.models.user import UserRepository

class ChatRepository:
    @staticmethod
    def add_friend(user_id, friend_id):
        with get_connection() as conn:
            try:
                conn.execute("INSERT INTO chat_friends (user_id, friend_id) VALUES (?, ?)", (user_id, friend_id))
                conn.execute("INSERT INTO chat_friends (user_id, friend_id) VALUES (?, ?)", (friend_id, user_id))
                return True
            except:
                return False
    
    @staticmethod
    def get_friends(user_id):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT u.* FROM users u 
                JOIN chat_friends f ON u.id = f.friend_id 
                WHERE f.user_id = ?
            """, (user_id,))
            return cursor.fetchall()
    
    @staticmethod
    def get_users_except(user_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE id != ?", (user_id,))
            return cursor.fetchall()
    
    @staticmethod
    def create_group(name, owner_id, announcement):
        with get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO chat_groups (name, owner_id, announcement) VALUES (?, ?, ?)
            """, (name, owner_id, announcement))
            group_id = cursor.lastrowid
            conn.execute("""
                INSERT INTO chat_group_members (group_id, user_id, is_admin) 
                VALUES (?, ?, 1)
            """, (group_id, owner_id))
            return group_id
    
    @staticmethod
    def get_groups(user_id):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT g.* FROM chat_groups g 
                JOIN chat_group_members m ON g.id = m.group_id 
                WHERE m.user_id = ? AND g.status = 'active'
            """, (user_id,))
            return cursor.fetchall()
    
    @staticmethod
    def add_group_member(group_id, user_id, is_admin=0):
        with get_connection() as conn:
            try:
                conn.execute("""
                    INSERT INTO chat_group_members (group_id, user_id, is_admin) 
                    VALUES (?, ?, ?)
                """, (group_id, user_id, is_admin))
                return True
            except:
                return False
    
    @staticmethod
    def get_group_members(group_id):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT u.*, m.is_admin FROM users u 
                JOIN chat_group_members m ON u.id = m.user_id 
                WHERE m.group_id = ?
            """, (group_id,))
            return cursor.fetchall()
    
    @staticmethod
    def get_group(group_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM chat_groups WHERE id = ?", (group_id,))
            return cursor.fetchone()
    
    @staticmethod
    def send_message(sender_id, target_id, target_type, content, message_type='text', file_url=None):
        with get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO chat_messages (sender_id, target_id, target_type, content, message_type, file_url) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (sender_id, target_id, target_type, content, message_type, file_url))
            return cursor.lastrowid
    
    @staticmethod
    def get_messages(target_id, target_type, limit=50):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT m.*, u.username as sender_name FROM chat_messages m 
                JOIN users u ON m.sender_id = u.id 
                WHERE m.target_id = ? AND m.target_type = ? 
                ORDER BY m.create_at DESC LIMIT ?
            """, (target_id, target_type, limit))
            return list(reversed(cursor.fetchall()))
    
    @staticmethod
    def get_all_groups():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM chat_groups")
            return cursor.fetchall()
    
    @staticmethod
    def update_group_status(group_id, status):
        with get_connection() as conn:
            conn.execute("UPDATE chat_groups SET status = ? WHERE id = ?", (status, group_id))
            return True
    
    @staticmethod
    def update_group_announcement(group_id, announcement):
        with get_connection() as conn:
            conn.execute("UPDATE chat_groups SET announcement = ? WHERE id = ?", (announcement, group_id))
            return True
    
    @staticmethod
    def get_all_files():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM chat_files ORDER BY upload_at DESC")
            return cursor.fetchall()
    
    @staticmethod
    def delete_group(group_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM chat_group_members WHERE group_id = ?", (group_id,))
            conn.execute("DELETE FROM chat_messages WHERE target_id = ? AND target_type = 'group'", (group_id,))
            conn.execute("DELETE FROM chat_groups WHERE id = ?", (group_id,))
            return True
