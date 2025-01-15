# Todo Application

This is a Todo application built with FastAPI for the backend and Angular for the frontend. The backend uses AWS DynamoDB for data storage, AWS SES for sending email notifications and PyDantic for config.

## Features

- Create, update, and delete tasks
- List all tasks
- Mark tasks as overdue and send email notifications
- Periodic task checking using APScheduler

## Prerequisites

- Python 3.10+
- Node.js and npm
- AWS account with DynamoDB and SES configured

## Backend Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/todo.git
    cd todo/backend
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up AWS credentials:**

    You can set the AWS credentials as environment variables:

    ```sh
    export AWS_ACCESS_KEY_ID='your_access_key_id'
    export AWS_SECRET_ACCESS_KEY='your_secret_access_key'
    export AWS_DEFAULT_REGION='your_region'
    export SES_FROM_EMAIL='your_sender_email'
    ```

    Alternatively, you can create a `.env` file in the root directory and add the credentials there:

    ```ini
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    AWS_DEFAULT_REGION=your_region
    SES_FROM_EMAIL=your_sender_email
    ```

    Pydantic will automatically load these environment variables.

5. **Run the backend server:**

    ```sh
    uvicorn app.main:app --reload
    ```

## Frontend Setup

1. **Navigate to the frontend directory:**

    ```sh
    cd ../frontend
    ```

2. **Install the dependencies:**

    ```sh
    npm install
    ```

3. **Run the frontend server:**

    ```sh
    ng serve
    ```

## Usage

- Access the frontend at `http://localhost:4200`
- Access the backend API documentation at `http://localhost:8000/docs`

## Project Structure
