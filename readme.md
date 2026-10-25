# AquaSmart AI Backend

A Django REST API backend for Aqua Company CRM. The system supports technician profile creation, department and job assignments, IOT and integration with a PostgreSQL database hosted on Supabase. It uses Docker for containerized development and deployment.

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Database Hosting:** Supabase
- **Containerization:** Docker, Docker Compose
- **Database Configuration:** `dj-database-url`, Psycopg 3
- **Python Version:** 3.12+

## Features

- **Technician Onboarding:** API endpoints for creating technician profiles and assigning departments and skills.
- **Database Integrity:** Atomic database transactions to maintain consistency across related database operations.
- **Company Association:** Supports associating technician profiles with the relevant company.
- **Supabase Integration:** Connects to a hosted PostgreSQL database using a configurable database connection URL.
- **Containerized Development:** Uses Docker Compose to simplify environment setup and application execution.
- **Live Code Updates:** Supports local development with mounted source code and Django's development server reloading.

## Project Structure

```text
aquasmart-ai/
├── config/                  # Django project settings and URL configuration
├── apps/                    # Application modules and business logic
├── Dockerfile               # Docker image configuration
├── docker-compose.yaml      # Docker Compose service configuration
├── requirements.txt         # Python dependencies
├── manage.py                # Django management utility
├── .env                     # Environment variables (not committed)
└── README.md                # Project documentation
```

## Prerequisites

Before setting up the project, ensure the following are installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- A Supabase project with a PostgreSQL database
- Git, if cloning the repository
- Python 3.12 or later, if running Django commands outside Docker

## Getting Started

### 1. Clone the Repository

Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/rahulv186/Aqua-Smart-CRM-Server.git
cd aquasmart-ai
```


### 2. Configure Environment Variables

Create a `.env` file in the project root directory.

```ini
DATABASE_URL=postgresql://postgres.<project-ref>:<password>@<pooler-host>:5432/postgres
SECRET_KEY=your_django_secret_key
DEBUG=True
```

Configure the variables as follows:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection URL for the Supabase database |
| `SECRET_KEY` | Django secret key used for cryptographic signing |
| `DEBUG` | Enables or disables Django debug mode |

Use the connection details provided by your Supabase project. If your Docker environment requires IPv4 connectivity, select a compatible Supabase connection method, such as the session pooler, where appropriate.

Do not commit the `.env` file or expose database credentials in source control.

### 3. Build and Start the Application

Run the following command from the project root:

```bash
docker compose up --build
```

Docker Compose will build the application image, install the required dependencies, and start the configured services.

Once the application has started, the API should be accessible at:

```text
http://127.0.0.1:8000/
```

The application supports live code updates if the Compose configuration mounts the local source directory and runs Django's development server.

To stop the running services, press `Ctrl+C`. To stop and remove the containers created by Compose, run:

```bash
docker compose down
```

## Database Migrations

Django migrations manage changes to the database schema.

### Apply Existing Migrations

With the application running, execute:

```bash
docker compose exec web python manage.py migrate
```

This applies pending migrations to the configured database. The Compose service must be named `web` for this command to work as written.

### Create New Migrations

After modifying Django models, generate migration files:

```bash
docker compose exec web python manage.py makemigrations
```

Apply the generated migrations:

```bash
docker compose exec web python manage.py migrate
```

Commit migration files to version control so that the database schema can be reproduced in other environments.

## Development

### Install Dependencies Locally

If you need to run Django commands outside Docker, create a virtual environment and install the project dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ensure the required environment variables are configured before running the application locally.

### Run Django Checks

To check the project configuration:

```bash
docker compose exec web python manage.py check
```

To view available Django management commands:

```bash
docker compose exec web python manage.py help
```

## Configuration and Security

- Keep `.env` files and database credentials out of version control.
- Use a strong, unique Django `SECRET_KEY`.
- Set `DEBUG=False` in production.
- Configure Django's `ALLOWED_HOSTS` and other production security settings appropriately.
- Use secure database connections and restrict database access to trusted services.
- Apply migrations carefully when working with a shared or production database.
- Do not expose Django's development server directly to the public internet in production.

