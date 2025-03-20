
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

Created by:-
Prashant Dhuri,
Harsh Dubey
