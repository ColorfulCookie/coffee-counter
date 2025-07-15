from flask import Flask, jsonify, request, send_from_directory, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
import sqlite3
import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")  # Set a secret key for session management
CORS(app)  # Enable CORS for all routes

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
USERNAME = os.getenv("COFFEE_USERNAME", "admin")
PASSWORD = os.getenv("COFFEE_PASSWORD", "password")

# Warn if default credentials are being used
default_credentials = USERNAME == "admin" and PASSWORD == "password"



DATABASE_NAME = os.getenv("COFFE_DB_NAME","coffee_log.db")
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

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == USERNAME:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            user = User(username)
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html', default_credentials=default_credentials)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return send_from_directory('.', 'coffee.html')

@app.route('/api/coffees', methods=['GET'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

@app.route('/api/export', methods=['GET'])
@login_required
def export_coffee_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp FROM coffee_entries ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        # Generate CSV content
        csv_content = "id,timestamp\n"
        for row in rows:
            csv_content += f"{row['id']},{row['timestamp']}\n"

        conn.close()

        # Serve the CSV content as a file
        return Response(csv_content, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=coffee_data.csv"})
    except Exception as e:
        print(f"Error during export: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/import', methods=['POST'])
@login_required
def import_coffee_data():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Get user preference for handling duplicates
        overwrite_duplicates = request.args.get('overwrite', 'false').lower() == 'true'

        # Read and process the CSV file
        conn = get_db_connection()
        cursor = conn.cursor()
        for line in file.stream.read().decode('utf-8').splitlines()[1:]:  # Skip header
            id, timestamp = line.split(',')
            if overwrite_duplicates:
                cursor.execute("INSERT OR REPLACE INTO coffee_entries (id, timestamp) VALUES (?, ?)", (id, timestamp))
            else:
                cursor.execute("INSERT OR IGNORE INTO coffee_entries (id, timestamp) VALUES (?, ?)", (id, timestamp))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Import successful'}), 200
    except Exception as e:
        print(f"Error during import: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure database exists
    setup_database()
    
    app.run(debug=True, host='localhost', port=5000)