import os
import logging
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
from werkzeug.utils import secure_filename

from utils.config import db_config

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    conn = psycopg2.connect(**db_config)
    return conn

def save_drawing(user_id, image_file, predictions):
    conn = create_connection()
    cur = conn.cursor()
    try:
        # Generate a unique filename
        filename = secure_filename(f"{uuid.uuid4()}.jpg")
        
        # Create the image path for database storage
        image_path = os.path.join('uploads', filename)
        
        logging.debug('in db.save_drawing()')
        logging.debug(f"upload folder: {current_app.config.get('UPLOAD_FOLDER')}")

        # Create the full path for file saving
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Insert the drawing with the image path and get the new drawing_id
        cur.execute(
            "INSERT INTO drawings (user_id, image_path) VALUES (%s, %s) RETURNING id",
            (user_id, image_path)
        )
        drawing_id = cur.fetchone()[0]
        
        # Save the file
        image_file.save(full_path)
        
        # Save predictions
        for pred, conf in predictions:
            cur.execute(
                "INSERT INTO predictions (drawing_id, prediction, confidence) VALUES (%s, %s, %s)",
                (drawing_id, pred, conf)
            )
        
        conn.commit()
        logging.info(f"Drawing saved successfully. ID: {drawing_id}, Path: {image_path}")
        return drawing_id, image_path
    except Exception as e:
        conn.rollback()
        logging.error(f"Error saving drawing: {str(e)}")
        raise e
    finally:
        cur.close()
        conn.close()

def get_drawings(user_id):
    conn = create_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT d.id, d.image_path, 
                   json_agg(json_build_array(p.prediction, p.confidence) ORDER BY p.confidence DESC) as predictions
            FROM drawings d
            LEFT JOIN predictions p ON d.id = p.drawing_id
            WHERE d.user_id = %s
            GROUP BY d.id
            ORDER BY d.created_at DESC
        """, (user_id,))
        drawings = cur.fetchall()
        logging.info(f"Retrieved {len(drawings)} drawings for user {user_id}")
        return drawings
    except Exception as e:
        logging.error(f"Error retrieving drawings for user {user_id}: {str(e)}")
        raise e
    finally:
        cur.close()
        conn.close()

def get_user(name):
    conn = create_connection()
    cur = conn.cursor()
    try:
        # Check if user already exists
        cur.execute("SELECT id FROM users WHERE name = %s", (name,))
        existing_user = cur.fetchone()
        
        if existing_user:
            # User already exists, return their id
            user_id = existing_user[0]
            logging.info(f"Existing user found. Name: {name}, ID: {user_id}")
            return user_id
        else:
            # User doesn't exist, create new user
            cur.execute("INSERT INTO users(name) VALUES(%s) RETURNING id", (name,))
            user_id = cur.fetchone()[0]
            conn.commit()
            logging.info(f"New user created. Name: {name}, ID: {user_id}")
            return user_id
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating/retrieving user {name}: {str(e)}")
        raise e
    finally:
        cur.close()
        conn.close()