# Sync Project

## Overview
Sync Service is a project designed to handle authentication and database connections using a serverless architecture. It utilizes AWS Lambda for executing functions and Docker for containerization.

## Project Structure
```
sync
├── authentication
│   └── auth.py          # Contains functions for password generation, token retrieval, and DB connection
├── lambda_function.py    # Entry point for AWS Lambda, contains the init method
├── Dockerfile            # Instructions for building the Docker image
├── docker-compose.yml    # Configuration for running the application in Docker
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone git@github.com:ln2khanal/api-postgres-datasync.git
   cd sync
   ```

2. **Build the Docker Image**
   ```bash
   docker build -t sync .
   ```

3. **Run the Application with Docker Compose**
   ```bash
   docker-compose up
   ```

## Usage
- The `init` method in `lambda_function.py` serves as the entry point for handling AWS Lambda events.
- The `auth.py` file provides necessary functions for authentication and database interactions.

## Dependencies
- Python 3.x
- Docker
- Docker Compose

## Contributing
Feel free to submit issues or pull requests for improvements or bug fixes. 

## License
This project is licensed under the MIT License.