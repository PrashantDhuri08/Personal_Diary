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
