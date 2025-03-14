# FastAPI Demo Project

### Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

### Installation

##### 1. Clone the repository

```bash
git clone https://github.com/trantudev/python_fastAPI_demo.git
cd python_fastAPI_demo
```

##### 2. Create a `.env` file

Create a `.env` file in the root directory of the project and add the following variables:

```bash
ADMIN_EMAIL=admindeptrai@gmail.com
ADMIN_NAME=Admin
ADMIN_PASSWORD=123456

POSTGRES_USER=user1
POSTGRES_PASSWORD=supersecretpassword
POSTGRES_DB=fastapi_demo
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

REDIS_HOST=redis
REDIS_PORT=6379
```

##### 3. Build and start the containers

```bash
docker-compose up -d
```

##### 4. Access the application

The fastapi application will be available at `http://localhost:8000`.

##### 5. API Documentation

Open your web browser and navigate to `http://localhost:8000/docs` to access the Swagger UI.
