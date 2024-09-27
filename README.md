Inventory Management System API

This project is a simple **Inventory Management System** built using **Django Rest Framework (DRF)**. It allows users to perform CRUD operations on inventory items, with JWT-based authentication for securing the API. The project uses **PostgreSQL** as the database, **Redis** for caching, and **Docker** for containerization.

## Documentation

This contains the whole documentaion of the api endpoints.

https://documenter.getpostman.com/view/32963641/2sAXqy3erU## Features

## Features

- **JWT Authentication**: Secure all endpoints with JSON Web Tokens (JWT).
- **CRUD Operations**: Create, read, update, and delete inventory items.
- **Redis Caching**: Frequently accessed items are cached to improve performance.
- **Error Handling**: Proper error codes and messages for failed operations.
- **Logging**: Integrated logging for debugging and monitoring.
- **Unit Tests**: Unit tests to ensure the correctness of the API functionality.
## Prerequisites

Ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)
Installation - Run 

Clone the project
```bash
  https://github.com/jishnu2040/inventory.git
```
setup env
```bash
  venv\Scripts\activate
```
Build and Run the Application
```bash
  docker-compose up --build

```
Run Database Migrations
```bash
  docker-compose exec web python manage.py migrate

```
Create a Superuser
```bash
  docker-compose exec web python manage.py createsuperuser
```
Run Unit Tests
```bash
  docker-compose exec web python manage.py test
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/jishnu2040/inventory.git
```

Go to the project directory

```bash
  cd inventory-management
```
Set Up a Virtual Environment

```bash
  # For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate

```

Install dependencies

```bash
  pip install -r requirements.txt
```
Set Up PostgreSQL Database

Set Up Redis

Apply Migrations

```bash
  python manage.py migrate
```
Create a Superuser (Optional)

```bash
  python manage.py createsuperuser

```

Start the server

```bash
  python manage.py runserver

```


## Tech Stack

Client: PostMan

Server: Django REST, Celery, JWT, Docker
## Authors

Jishnuraj R S
