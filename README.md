# Cibus API made with Flask

## Initial Setup

Virtual environment creation
```python3.11 -m venv .venv```

(Select interpretor with Cmd+Shift+P)


Install dependecies
```pip install -r requirements.txt```


## Run Dockerfile in local

```
docker build -t cibus_api:latest . 
```
```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" cibus_api
```
