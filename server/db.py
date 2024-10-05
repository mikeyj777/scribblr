import os
import sys
from flask import current_app
from psycopg2.extras import RealDictCursor

import psycopg2
from utils.config import db_config

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    conn = psycopg2.connect(**db_config)
    return conn

def get_user(name):
    conn = create_connection()
    cur = conn.cursor()
    
    # First, check if the user already exists
    cur.execute("SELECT id FROM users WHERE name = %s", (name,))
    existing_user = cur.fetchone()
    
    logging.debug(f"Checking if user {name} exists.  Result: {existing_user}")

    if existing_user:
        # User already exists, return their id
        logging.debug(f"User {name} already exists.  Returning id: {existing_user[0]}")
        user_id = existing_user[0]
    else:
        # User doesn't exist, create new user
        cur.execute("INSERT INTO users(name) VALUES(%s) RETURNING id", (name,))
        user_id = cur.fetchone()[0]
        conn.commit()
    
    cur.close()
    conn.close()
    
    return user_id

def save_drawing(user_id, image_file, predictions):
    conn = create_connection()
    cur = conn.cursor()
    try:
        # Save the drawing
        cur.execute(
            "INSERT INTO drawings (user_id, image_path) VALUES (%s, %s) RETURNING id",
            (user_id, "")
        )
        drawing_id = cur.fetchone()[0]
        
        # Update the image path with the drawing ID
        image_path = f"uploads/{drawing_id}.jpg"
        cur.execute(
            "UPDATE drawings SET image_path = %s WHERE id = %s",
            (image_path, drawing_id)
        )
        
        # Save the image file
        image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f"{drawing_id}.jpg"))
        
        # Save predictions
        for pred, conf in predictions:
            cur.execute(
                "INSERT INTO predictions (drawing_id, prediction, confidence) VALUES (%s, %s, %s)",
                (drawing_id, pred, conf)
            )
        
        conn.commit()
        return drawing_id
    finally:
        cur.close()
        conn.close()

def get_drawings(user_id):
    conn = create_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT d.id, d.image_path, 
                   json_agg(json_build_array(p.prediction, p.confidence)) as predictions
            FROM drawings d
            LEFT JOIN predictions p ON d.id = p.drawing_id
            WHERE d.user_id = %s
            GROUP BY d.id
            ORDER BY d.created_at DESC
        """, (user_id,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()