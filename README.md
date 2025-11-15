# ToDo List API

A simple ToDo List API built with Django and Django REST Framework. This project allows users to manage their to-do items through a set of RESTful endpoints.

Project idea from: [roadmap.sh/projects/todo-list-api](https://roadmap.sh/projects/todo-list-api)

## Features

*   **User Authentication**: Secure user registration and login using JSON Web Tokens (JWT).
*   **CRUD Operations**: Full Create, Read, Update, and Delete functionality for to-do items.
*   **Ownership**: Users can only view and modify their own to-do items.
*   **Filtering and Searching**: Filter todos by completion status and search by title or description.
*   **Ordering**: Sort todos based on creation date, title, or completion status.
*   **API Throttling**: Rate limiting for both anonymous and authenticated users to prevent abuse.

## Prerequisites

*   Python 3.8+
*   pip
*   virtualenv (recommended)

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd "ToDo API"
    ```

2.  **Create and activate a virtual environment:**

    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

Here is a list of the available API endpoints.

### Authentication

*   `POST /register/`
    *   **Description**: Register a new user.
    *   **Body**: `{ "name": "Your Name", "email": "user@example.com", "password": "yourpassword" }`

*   `POST /login/`
    *   **Description**: Log in to receive JWT access and refresh tokens.
    *   **Body**: `{ "email": "user@example.com", "password": "yourpassword" }`

*   `POST /refresh/`
    *   **Description**: Obtain a new access token using a refresh token.
    *   **Body**: `{ "refresh": "your_refresh_token" }`

### ToDo Items

*All ToDo endpoints require authentication.*

*   `GET /todos/`
    *   **Description**: Get the list of todos for the authenticated user. Supports filtering, searching, and ordering.
*   `POST /todos/`
    *   **Description**: Create a new todo item.
    *   **Body**: `{ "title": "New Todo", "description": "A description for the new todo." }`
*   `GET /todos/<int:todo_id>/`
    *   **Description**: Retrieve a specific todo item.
*   `PUT /todos/<int:todo_id>/`
    *   **Description**: Update a specific todo item.
*   `DELETE /todos/<int:todo_id>/`
    *   **Description**: Delete a specific todo item.
*   `PUT /todos/<int:todo_id>/complete/`
    *   **Description**: Toggle the completion status of a todo item.