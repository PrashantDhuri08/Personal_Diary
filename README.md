
# Personal Diary Application

A web-based personal diary application with Streamlit frontend and Python backend.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher

### Automatic Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Run the setup script:


4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

### Manual Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Ensure the virtual environment is activated
2. Start the backend server:
```bash
cd backend
python app.py
```
3. In a new terminal (with environment activated), start the frontend:
```bash
cd frontend
streamlit run app.py
```
4. Open your browser to http://localhost:8501

## Development

- Backend API runs on: http://localhost:5000/api
- Frontend runs on: http://localhost:8501

# Personal Diary Application

## Overview
The **Personal Diary App** is a web-based application built using **Streamlit** for the frontend and **Flask** for the backend. It provides users with a secure and intuitive platform to record and manage their personal thoughts, daily activities, and notes.

## Features
- **Diary Entry Management** – Create, edit, and delete diary entries.
- **Search & Filter** – Easily find past entries using search filters.
- **Data Persistence** – Stores entries securely using a database.
- **Interactive UI** – A clean and user-friendly interface powered by Streamlit.

## Technologies Used
- **Frontend:** Streamlit
- **Backend:** Flask
- **Database:** SQLite

This app provides a seamless experience for users who want to maintain a digital personal diary with ease.

# Setup and installation to run this project

## 1. Install `virtualenv`

```sh
pip install virtualenv
```

## 2. Create a Virtual Environment

```sh
python -m venv env
```

## 3. Activate the Virtual Environment

On Windows:

```sh
env\Scripts\activate
```

On macOS/Linux:

```sh
source env/bin/activate
```

## 4. Install Required Dependencies

```sh
pip install -r requirements.txt
```

## 5. Run the Project

### Run the API

```sh
cd backend
python diary_api.py
```

### Run the Frontend (on seperate terminal)

```sh
cd frontend
python app.py
```

## Running the Application

You can start both the frontend and backend with a single command:

```
run-app.bat
```

### Manual Start

To run the parts individually:

#### Frontend
```
cd frontend
npm start
```

#### Backend
```
cd backend
npm start
```

Created by:-
Prashant Dhuri,
Harsh Dubey
