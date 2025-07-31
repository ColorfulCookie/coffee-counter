import sqlite3
import datetime
import os

# --- Configuration ---
DATABASE_NAME = os.getenv("COFFEE_DB_NAME", "coffee_log.db")
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), DATABASE_NAME))

def setup_database():
    """
    Sets up the SQLite database and the 'coffee_entries' table if they don't exist.
    The database file will be created in the same directory as the script.
    """
    try:
        # Connect to the SQLite database.
        # If the database file doesn't exist, it will be created.
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Create the table if it doesn't already exist
        # id: A unique identifier for each coffee entry (automatically increments)
        # timestamp: The date and time when the coffee was logged
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coffee_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during setup: {e}")
        raise
    finally:
        if conn:
            conn.close()

def log_coffee():
    """
    Logs a new coffee entry with the current timestamp into the database.
    Returns the timestamp of the logged coffee.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Get the current date and time
        current_time = datetime.datetime.now()
        # Format it as a string (YYYY-MM-DD HH:MM:SS)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Insert the new coffee entry
        cursor.execute("INSERT INTO coffee_entries (timestamp) VALUES (?)", (formatted_time,))
        conn.commit()
        return formatted_time
    except sqlite3.Error as e:
        print(f"Database error while logging coffee: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_total_coffees():
    """
    Retrieves the total number of coffee entries from the database.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM coffee_entries")
        count = cursor.fetchone()[0] # fetchone() returns a tuple, e.g., (5,)
        return count
    except sqlite3.Error as e:
        print(f"Database error while getting total coffees: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def main():
    """
    Main function to run the coffee logger.
    """
    print("Coffee Logger Deluxe ☕")
    print("----------------------")

    # Ensure the database and table are set up
    setup_database()

    # Log a new coffee
    logged_time = log_coffee()

    if logged_time:
        total_coffees = get_total_coffees()
        print(f"\n✅ Coffee successfully logged at: {logged_time}")
        print(f"🎉 Total coffees consumed: {total_coffees}")
    else:
        print("\n❌ Failed to log coffee.")


if __name__ == "__main__":
    # This ensures the main() function is called only when the script is executed directly
    # (not when imported as a module).
    main()
