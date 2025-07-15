from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Use the same database configuration as coffee.py
DATABASE_NAME = "coffee_log.db"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(SCRIPT_DIR, DATABASE_NAME)

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """
    Sets up the SQLite database and tables if they don't exist.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Create the coffee_entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coffee_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL
            )
        ''')
        
        # Create the session_counter table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_counter (
                id INTEGER PRIMARY KEY,
                count INTEGER NOT NULL DEFAULT 0
            )
        ''')
        
        # Initialize session counter if it doesn't exist
        cursor.execute("SELECT COUNT(*) FROM session_counter WHERE id = 1")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO session_counter (id, count) VALUES (1, 0)")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during setup: {e}")
    finally:
        if conn:
            conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'coffee.htm')

@app.route('/api/coffees', methods=['GET'])
def get_coffees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp FROM coffee_entries ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        
        coffees = []
        for row in rows:
            coffees.append({
                'id': row['id'],
                'timestamp': row['timestamp']
            })
        
        conn.close()
        return jsonify(coffees)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/coffees', methods=['POST'])
def log_coffee():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("INSERT INTO coffee_entries (timestamp) VALUES (?)", (formatted_time,))
        
        # Update session counter
        cursor.execute("UPDATE session_counter SET count = count + 1 WHERE id = 1")
        
        conn.commit()
        
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'id': new_id,
            'timestamp': formatted_time
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/coffees/<int:coffee_id>', methods=['PUT'])
def update_coffee(coffee_id):
    try:
        data = request.json
        new_timestamp = data.get('timestamp')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE coffee_entries SET timestamp = ? WHERE id = ?", 
                      (new_timestamp, coffee_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/coffees/<int:coffee_id>', methods=['DELETE'])
def delete_coffee(coffee_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM coffee_entries WHERE id = ?", (coffee_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session-counter', methods=['GET'])
def get_session_counter():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM session_counter WHERE id = 1")
        result = cursor.fetchone()
        count = result['count'] if result else 0
        conn.close()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session-counter', methods=['POST'])
def reset_session_counter():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE session_counter SET count = 0 WHERE id = 1")
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure database exists
    setup_database()
    
    app.run(debug=True, host='localhost', port=5000)