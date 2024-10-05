import psycopg2
from utils.config import db_config

def create_connection():
    conn = psycopg2.connect(**db_config)
    return conn

def create_user(name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name) VALUES(%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()

def save_drawing(name, image_file, predictions):
    image_path = f"uploads/{image_file.filename}"
    image_file.save(image_path)
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO drawings(user_id, image_path, predictions) VALUES((SELECT id FROM users WHERE name = %s), %s, %s)",
        (name, image_path, predictions)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_drawings(name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM drawings WHERE user_id = (SELECT id FROM users WHERE name = %s)",
        (name,)
    )
    drawings = cur.fetchall()
    cur.close()
    conn.close()
    return drawings