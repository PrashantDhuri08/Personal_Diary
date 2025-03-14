## Backend

### Dependencies and Software Required

1. **Flask**: A micro web framework for Python.
2. **SQLite**: A lightweight database used for storing diary entries.
3. **Datetime**: A module for manipulating dates and times.

### API Endpoints

1. **Create a new diary entry (POST)**: `/api/entries`
2. **Read all diary entries (GET)**: `/api/entries`
3. **Read a single diary entry by ID (GET)**: `/api/entries/<int:entry_id>`
4. **Update an existing diary entry (PUT)**: `/api/entries/<int:entry_id>`
5. **Delete a diary entry (DELETE)**: `/api/entries/<int:entry_id>`

### Environment Setup

1. **Python Environment**: Create a virtual environment and install the required dependencies.

```bash
# filepath: c:\Users\Harsh D Dubey\Personal_Diary\backend\temp.md
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Install dependencies
pip install Flask sqlite3 datetime
```
