## Frontend

### Dependencies and Software Required

1. **HTML/CSS/JavaScript**: Basic web technologies for building the frontend.
2. **React.js**: A JavaScript library for building user interfaces.
3. **Axios**: A promise-based HTTP client for making requests to the backend API.
4. **Bootstrap**: A CSS framework for responsive design.

### Backend

The backend is built using Python and Flask. It provides a RESTful API for managing diary entries.

#### Dependencies

1. **Flask**: A micro web framework for Python.
2. **SQLite**: A lightweight database used for storing diary entries.
3. **Datetime**: A module for manipulating dates and times.

### Environment Setup

1. **Python Environment**: Create a virtual environment and install the required dependencies.

```bash
# filepath: c:\Users\Harsh D Dubey\Personal_Diary\frontend\temp.md
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

2. **Frontend Setup**: Initialize a React project and install the required dependencies.

```bash
# filepath: c:\Users\Harsh D Dubey\Personal_Diary\frontend\temp.md
# Initialize a React project
npx create-react-app personal-diary-frontend

# Navigate to the project directory
cd personal-diary-frontend

# Install Axios and Bootstrap
npm install axios bootstrap
```
