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
