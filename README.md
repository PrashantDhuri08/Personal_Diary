
# Personal Diary App

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

## 2. Navigate to Backend Directory

```sh
cd backend
```

## 3. Create a Virtual Environment

```sh
python -m venv env
```

## 4. Activate the Virtual Environment

On Windows:

```sh
env\Scripts\activate
```

On macOS/Linux:

```sh
source env/bin/activate
```

### Check if SQLite is present in your env if not then you have to install it first

## 5. Install Required Dependencies

```sh
pip install -r requirements.txt
```

## 6. Run the Project

### Run the API

```sh
python diary_api.py
```

### Run the Frontend (on seperate terminal)

```sh
python app.py
```
