# A CRUD API to Practice Flask and Python

## Project Requirements

The _Practice CRUD API_ uses __Python 3.8__.

## Project Setup

```ps1
# Virtual environment:
py -m venv .venv
./.venv/Scripts/Activate.ps1

# Installing project dependencies:
pip install -r requirements.txt
```

## Run the Tests

```ps1
# Tests:
pytest

# Tests with coverage:
coverage run -m pytest ; coverage report
```

## Run the App

```ps1
# Start the development server:
$Env:FLASK_DEBUG = 1 ; flask run
```
