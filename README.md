# Test darwin

## Introduction

This project is a Django-based web application containerized using Docker. It utilizes PostgreSQL as the database backend.

## Features

- Django application
- PostgreSQL database
- Docker for containerization
- Pre-configured `docker-compose.yml` for easy setup
- Automated database migrations and static file collection

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### Step 1: Clone the Repository

```sh
git clone https://github.com/Egor1511/darwin.git
cd darwin
```

### Step 2: Build and Run the Docker Containers

```sh
docker-compose up --build
```
```sh
docker-compose exec web python manage.py migrate
```

This command will:

1. Build the Docker images.
2. Start the PostgreSQL database container.
3. Start the Django application container.
4. Apply database migrations.
6. Run the Django application using Gunicorn.

### Step 3: Access the Application

After the containers are up and running, the application should be accessible at:

```
http://127.0.0.1/
```

## Postman Collection

We have created a Postman collection named **Test Solutions** for testing the API endpoints.

### Instructions to Run Postman Collection

1. Fork the Postman collectionur-collection to your own Postman workspace.

```
https://www.postman.com/supply-cosmologist-43454487/workspace/github-test-tasks/collection/31564096-430f8224-493f-4aa0-81be-afd82289786f
```
3. Set up the Postman environment variables as needed (e.g., `base_url` to `http://localhost:8000`).
4. Run the requests in the collection on your local machine.

### Postman Collection Link

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/supply-cosmologist-43454487/workspace/github-test-tasks/collection/31564096-430f8224-493f-4aa0-81be-afd82289786f))

## Environment Variables

The following environment variables are used in the project. Make sure to set them accordingly in your `.env` file or in the Docker Compose file:

- `POSTGRES_DB`: The name of the PostgreSQL database.
- `POSTGRES_USER`: The PostgreSQL database user.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database user.
- `POSTGRES_HOST`: The host address for the PostgreSQL database (default is `db` when using Docker Compose).
- `POSTGRES_PORT`: The port for the PostgreSQL database (default is `5432`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## Contact

For any inquiries or support, please contact `https://t.me/EFirraa`.
