# FastAPI Celery Notification Service

This project is a FastAPI application that uses Celery for asynchronous task processing to send notifications.

## Architecture Overview

The application consists of the following components:

-   **FastAPI Application:** A Python web framework for building APIs.
-   **PostgreSQL:** A relational database to store the application data.
-   **Celery:** An asynchronous task queue/job queue based on distributed message passing.
-   **CloudAMQP:** A cloud-based RabbitMQ service that Celery uses to pass messages between the API and the workers.
-   **SendGrid:** An email delivery service to send notifications.

The overall architecture is illustrated in the `related/architecture.excalidraw` file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Docker
-   Docker Compose
-   A CloudAMQP account

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd FastAPI-Celery-NotificationService
    ```

2.  **Environment Variables:**

    Create a `.env` file in the root of the project and add the following environment variables:

    ```
    CELERY_BROKER_URL=<your-cloudamqp-url>
    SENDGRID_API_KEY=<your-sendgrid-api-key>
    # Add other necessary environment variables from docker-compose.yaml
    ```

### Running the Application

The application has two main components that need to be run separately: the API and the Celery worker.

1.  **Run the API and Database with Docker Compose:**

    This command will build the Docker image for the API and start the `api` and `db` services.

    ```bash
    docker compose -f docker/docker-compose.yaml up --build
    ```

2.  **Run the Celery Worker:**

    The Celery worker needs to be run in a separate terminal. Make sure you have the necessary dependencies installed locally.

    The command to run the worker is defined in `.vscode/launch.json`:

    ```bash
    celery -A app.workers.send_email worker -Q send-email --loglevel=info -c 1 --without-heartbeat --without-gossip --without-mingle
    ```

    This command starts a Celery worker that connects to the CloudAMQP broker and listens to the `send-email` queue.

### How it Works

1.  The client interacts with the **FastAPI API** to perform operations like creating users, managing products, carts, and orders.
2.  The API and the data are managed by the **Docker Compose** setup, which includes the API container and a **PostgreSQL** database container.
3.  When an order is created, confirmed, or canceled, the API sends a message to the **CloudAMQP** message broker.
4.  The **Celery worker**, running in a separate process, picks up the message from the queue.
5.  The worker processes the message and uses **SendGrid** to send an email notification to the user.
