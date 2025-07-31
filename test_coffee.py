#!/usr/bin/env python3
"""
Simple tests for coffee counter functionality.
"""
import os
import tempfile
import unittest
import sqlite3
from unittest.mock import patch

# Import our modules
import coffee


class TestCoffeeCounter(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment with temporary database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.test_db_path = self.temp_db.name
        
        # Patch the DATABASE_PATH for testing
        self.patcher = patch.object(coffee, 'DATABASE_PATH', self.test_db_path)
        self.patcher.start()
    
    def tearDown(self):
        """Clean up test environment."""
        self.patcher.stop()
        try:
            os.unlink(self.test_db_path)
        except OSError:
            pass
    
    def test_database_setup(self):
        """Test that database setup creates the correct table."""
        coffee.setup_database()
        
        # Verify table exists and has correct structure
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coffee_entries'")
        table_exists = cursor.fetchone() is not None
        self.assertTrue(table_exists, "coffee_entries table should exist")
        
        # Check table structure
        cursor.execute("PRAGMA table_info(coffee_entries)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        self.assertIn('id', column_names, "Table should have 'id' column")
        self.assertIn('timestamp', column_names, "Table should have 'timestamp' column")
        
        conn.close()
    
    def test_log_coffee(self):
        """Test logging a coffee entry."""
        coffee.setup_database()
        
        # Log a coffee
        timestamp = coffee.log_coffee()
        self.assertIsNotNone(timestamp, "log_coffee should return a timestamp")
        
        # Verify it was stored in database
        total = coffee.get_total_coffees()
        self.assertEqual(total, 1, "Should have 1 coffee logged")
    
    def test_get_total_coffees(self):
        """Test getting total coffee count."""
        coffee.setup_database()
        
        # Initially should be 0
        total = coffee.get_total_coffees()
        self.assertEqual(total, 0, "Initial count should be 0")
        
        # Log some coffees
        coffee.log_coffee()
        coffee.log_coffee()
        
        total = coffee.get_total_coffees()
        self.assertEqual(total, 2, "Should have 2 coffees logged")
    
    def test_multiple_coffee_logging(self):
        """Test logging multiple coffee entries."""
        coffee.setup_database()
        
        # Log multiple coffees
        timestamps = []
        for _ in range(5):
            timestamp = coffee.log_coffee()
            timestamps.append(timestamp)
        
        # All should be successful
        self.assertEqual(len([t for t in timestamps if t is not None]), 5)
        
        # Total should be 5
        total = coffee.get_total_coffees()
        self.assertEqual(total, 5, "Should have 5 coffees logged")


if __name__ == '__main__':
    unittest.main()