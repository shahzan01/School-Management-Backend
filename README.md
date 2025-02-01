# Application Usage Guide

## Prerequisites
- **Python 3.12**
- [Virtualenv](https://virtualenv.pypa.io/) (for non-Docker setup)
- **Docker** (optional, for Docker-based usage)

---
## With Docker

### Prerequisites

Make sure you have Docker installed on your system. If not, you can download and install it from [here](https://www.docker.com/get-started).

### 1. Pull the Docker Image
To pull the image from Docker Hub, run the following command:
```bash
docker pull shahzan1/flask-app:v1
```

### 2. Run the Container
After pulling the image, you can run the Flask app in a container. Use the following command to start it:
```bash
docker run -it -p 5000:5000 shahzan1/flask-app:v1
```
* This runs the container.
* It maps port 5000 on your local machine to port 5000 in the container, assuming your Flask app runs on port 5000.


### 3. Run the Server
Inside the container, you can run:
```bash
bash run.sh  # Launches the Flask app
```
### 4. Run Tests in Docker
To run tests inside the container, use:
```bash
pytest -vvv -s tests/
```

### 5. Generate Test Coverage in Docker
To generate the test coverage report inside the container, use:
```bash
pytest --cov
```


Notes
* Replace port mappings (e.g., 5000:5000) in docker-compose.yml if conflicts arise.
* Configure environment variables (if needed) in .env or docker-compose.yml.
















---

## Without Docker

### 1. Install Requirements
Create and activate a virtual environment, then install dependencies:
```bash
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```

### 2. Initialize the Database
```bash
export FLASK_APP=core/server.py
rm -f core/store.sqlite3  # Remove existing database (if any)
flask db upgrade -d core/migrations/  # Create fresh database
```
### 3. Start the Server
```bash
bash run.sh  # Launches the Flask app
```

### 4. Run Tests
```bash
pytest -vvv -s tests/
```
### 5. Generate Test Coverage Report
```bash
pytest --cov
open htmlcov/index.html  # View coverage report in your browser
```


















