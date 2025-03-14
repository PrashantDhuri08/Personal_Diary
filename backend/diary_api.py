from flask import Flask, request, jsonify, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

#connecting db
def initialize_database():
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date_created TEXT NOT NULL,
            archived INTEGER DEFAULT 0
        )
    ''')
    # Check if the 'archived' column exists, and add it if it doesn't
    cursor.execute("PRAGMA table_info(entries)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'archived' not in columns:
        cursor.execute('ALTER TABLE entries ADD COLUMN archived INTEGER DEFAULT 0')
    conn.commit()
    conn.close()

def get_entries(archived=0):
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE archived = ?', (archived,))
    rows = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'title': row[1], 'content': row[2], 'date_created': row[3]} for row in rows]

# API Endpoints

# 1. Create a new diary entry (POST)
@app.route('/api/entries', methods=['POST'])
def add_entry():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO entries (title, content, date_created) VALUES (?, ?, ?)',
                   (title, content, date_created))
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'message': 'Entry added successfully', 'id': entry_id}), 201

# 2. Read all diary entries (GET)
@app.route('/api/entries', methods=['GET'])
def view_entries():
    entries = get_entries()
    return jsonify({'entries': entries}), 200

# 3. Read a single diary entry by ID (GET)
@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    conn.close()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    return jsonify({'id': entry[0], 'title': entry[1], 'content': entry[2], 'date_created': entry[3]}), 200

# 4. Update an existing diary entry (PUT)
@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    data = request.get_json()
    new_title = data.get('title')
    new_content = data.get('content')
    
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        conn.close()
        return jsonify({'error': 'Entry not found'}), 404
    
    # Use existing values if new ones aren't provided
    title = new_title if new_title else entry[1]
    content = new_content if new_content else entry[2]
    
    cursor.execute('UPDATE entries SET title = ?, content = ? WHERE id = ?',
                   (title, content, entry_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': f'Entry ID {entry_id} updated successfully'}), 200

# 5. Delete a diary entry (DELETE)
@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        conn.close()
        return jsonify({'error': 'Entry not found'}), 404
    
    cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': f'Entry ID {entry_id} deleted successfully'}), 200

# 6. Archive a diary entry (POST)
@app.route('/api/archive_entry/<int:entry_id>', methods=['POST'])
def archive_entry(entry_id):
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        conn.close()
        return jsonify({'error': 'Entry not found'}), 404
    
    cursor.execute('UPDATE entries SET archived = 1 WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': f'Entry ID {entry_id} archived successfully'}), 200

# 7. Read all archived diary entries (GET)
@app.route('/api/archived_entries', methods=['GET'])
def view_archived_entries():
    entries = get_entries(archived=1)
    return jsonify({'entries': entries}), 200

# 8. Send a diary entry (POST)
@app.route('/api/send_entry/<int:entry_id>', methods=['POST'])
def send_entry(entry_id):
    # Placeholder for sending logic
    # Implement the logic to send the entry (e.g., via email or other means)
    return jsonify({'message': f'Entry ID {entry_id} sent successfully'}), 200

# Add a root route to redirect to /api/entries
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Personal Diary API',
        'endpoints': {
            'GET /api/entries': 'Get all diary entries',
            'POST /api/entries': 'Create a new diary entry',
            'GET /api/entries/<id>': 'Get a specific diary entry',
            'PUT /api/entries/<id>': 'Update a diary entry',
            'DELETE /api/entries/<id>': 'Delete a diary entry',
            'POST /api/archive_entry/<id>': 'Archive a diary entry',
            'GET /api/archived_entries': 'Get all archived entries',
            'POST /api/send_entry/<id>': 'Send a diary entry'
        }
    }), 200

# Add a route for /api to provide API information
@app.route('/api', methods=['GET'])
def api_info():
    return redirect('/')

# Initialize the database and run the app
if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5000)