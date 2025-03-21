from flask import Flask, request, jsonify, redirect
import sqlite3
from datetime import datetime
import functools

app = Flask(__name__)

# Global database connection pool
DB_CONNECTION = None

# Optimize database connection with a decorator
def with_db_connection(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('diary.db')
        try:
            conn.row_factory = sqlite3.Row
            kwargs['conn'] = conn
            return f(*args, **kwargs)
        finally:
            conn.close()
    return wrapper

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
            archived INTEGER DEFAULT 0,
            pinned INTEGER DEFAULT 0,
            tags TEXT DEFAULT ''
        )
    ''')
    # Check if the 'archived' column exists, and add it if it doesn't
    cursor.execute("PRAGMA table_info(entries)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'archived' not in columns:
        cursor.execute('ALTER TABLE entries ADD COLUMN archived INTEGER DEFAULT 0')
    if 'pinned' not in columns:
        cursor.execute('ALTER TABLE entries ADD COLUMN pinned INTEGER DEFAULT 0')
    if 'tags' not in columns:
        cursor.execute('ALTER TABLE entries ADD COLUMN tags TEXT DEFAULT ""')
    
    # Add index for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_archived ON entries(archived)')
    
    conn.commit()
    conn.close()

@with_db_connection
def get_entries(archived=0, conn=None):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE archived = ?', (archived,))
    rows = cursor.fetchall()
    entries = []
    for row in rows:
        entry = dict(row)
        # Convert tags string to list if it exists
        if entry.get('tags'):
            try:
                entry['tags'] = entry['tags'].split(',')
            except:
                entry['tags'] = []
        entries.append(entry)
    return entries

# API Endpoints

# 1. Create a new diary entry (POST)
@app.route('/api/entries', methods=['POST'])
@with_db_connection
def add_entry(conn=None):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags', [])
    pinned = data.get('pinned', False)
    
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    cursor = conn.cursor()
    date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Convert tags list to comma-separated string
    tags_str = ','.join(tags) if tags else ''
    
    cursor.execute('INSERT INTO entries (title, content, date_created, pinned, tags) VALUES (?, ?, ?, ?, ?)',
                   (title, content, date_created, 1 if pinned else 0, tags_str))
    conn.commit()
    entry_id = cursor.lastrowid
    
    return jsonify({'message': 'Entry added successfully', 'id': entry_id}), 201

# 2. Read all diary entries (GET)
@app.route('/api/entries', methods=['GET'])
@with_db_connection
def view_entries(conn=None):
    entries = get_entries(archived=0, conn=conn)
    return jsonify({'entries': entries}), 200

# 3. Read a single diary entry by ID (GET)
@app.route('/api/entries/<int:entry_id>', methods=['GET'])
@with_db_connection
def get_entry(entry_id, conn=None):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    result = {
        'id': entry[0], 
        'title': entry[1], 
        'content': entry[2], 
        'created_at': entry[3],
        'archived': bool(entry[4]),
        'pinned': bool(entry[5])
    }
    
    # Add tags if they exist
    if len(entry) > 6 and entry[6]:
        result['tags'] = entry[6].split(',')
    else:
        result['tags'] = []
        
    return jsonify(result), 200

# 4. Update an existing diary entry (PUT)
@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
@with_db_connection
def update_entry(entry_id, conn=None):
    data = request.get_json()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    # Use existing values if new ones aren't provided
    title = data.get('title', entry[1])
    content = data.get('content', entry[2])
    archived = data.get('archived', bool(entry[4]))
    pinned = data.get('pinned', bool(entry[5]))
    
    # Handle tags
    if 'tags' in data and isinstance(data['tags'], list):
        tags_str = ','.join(data['tags'])
    elif len(entry) > 6:
        tags_str = entry[6]
    else:
        tags_str = ''
    
    cursor.execute('''
        UPDATE entries 
        SET title = ?, content = ?, archived = ?, pinned = ?, tags = ? 
        WHERE id = ?
    ''', (title, content, 1 if archived else 0, 1 if pinned else 0, tags_str, entry_id))
    
    conn.commit()
    
    return jsonify({'message': f'Entry ID {entry_id} updated successfully'}), 200

# 5. Delete a diary entry (DELETE)
@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
@with_db_connection
def delete_entry(entry_id, conn=None):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    conn.commit()
    
    return jsonify({'message': f'Entry ID {entry_id} deleted successfully'}), 200

# 6. Archive a diary entry (POST)
@app.route('/api/archive_entry/<int:entry_id>', methods=['POST'])
@with_db_connection
def archive_entry(entry_id, conn=None):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    cursor.execute('UPDATE entries SET archived = 1 WHERE id = ?', (entry_id,))
    conn.commit()
    
    return jsonify({'message': f'Entry ID {entry_id} archived successfully'}), 200

# New endpoint: Unarchive a diary entry (POST)
@app.route('/api/unarchive_entry/<int:entry_id>', methods=['POST'])
@with_db_connection
def unarchive_entry(entry_id, conn=None):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    cursor.execute('UPDATE entries SET archived = 0 WHERE id = ?', (entry_id,))
    conn.commit()
    
    return jsonify({'message': f'Entry ID {entry_id} unarchived successfully'}), 200

# 7. Read all archived diary entries (GET)
@app.route('/api/archived_entries', methods=['GET'])
@with_db_connection
def view_archived_entries(conn=None):
    entries = get_entries(archived=1, conn=conn)
    return jsonify({'entries': entries}), 200

# 8. Send a diary entry (POST)
@app.route('/api/send_entry/<int:entry_id>', methods=['POST'])
@with_db_connection
def send_entry(entry_id, conn=None):
    # Placeholder for sending logic
    # Implement the logic to send the entry (e.g., via email or other means)
    return jsonify({'message': f'Entry ID {entry_id} sent successfully'}), 200

# 9. Pin/Unpin a diary entry (PUT)
@app.route('/api/entries/<int:entry_id>/pin', methods=['PUT'])
@with_db_connection
def toggle_pin(entry_id, conn=None):
    data = request.get_json()
    pinned = data.get('pinned', False)
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    cursor.execute('UPDATE entries SET pinned = ? WHERE id = ?', (1 if pinned else 0, entry_id))
    conn.commit()
    
    return jsonify({'message': f'Entry ID {entry_id} {"pinned" if pinned else "unpinned"} successfully'}), 200

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

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
            'POST /api/unarchive_entry/<id>': 'Unarchive a diary entry',
            'GET /api/archived_entries': 'Get all archived entries',
            'POST /api/send_entry/<id>': 'Send a diary entry',
            'PUT /api/entries/<id>/pin': 'Pin/Unpin a diary entry',
            'GET /api/health': 'Health check'
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