from app.db.database import get_connection

conn = get_connection()

print("CONNECTED")

conn.close()