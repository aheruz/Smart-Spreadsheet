# README

## Project Overview

This repository contains two main projects:

1. **Python Service**: Handles the core logic for creating assistants, uploading files, and attaching files to the assistants. It processes Excel files, generates JSON, and uploads this JSON to the vector database provided by OpenAI.

2. **Node Application**: Acts as the front-end, managing chat functions. Users can upload files through the UI, but these requests are forwarded to the Python service, which handles the file processing and data management.

## Requirements

Please refer to [REQUIREMENTS.md](REQUIREMENTS.md) for detailed information on the initial goals of the project.

## Setup Instructions

### Environment Setup
Both services require specific environment variables to be set up. Below are the steps to configure the environment:

1. **Python Service**:
   - Set up the `.env.local` for the Python service.

2. **Node Application**:
   - Set up the `.env.local` for the Node application.
   - Ensure that the `APP_API_URL` points to the Python service.

### Running the Services

1. **Python Service**:
   - Navigate to the Python service directory.
   - Run the service using the appropriate command (e.g., `python app.py`).

2. **Node Application**:
   - Navigate to the Node application directory.
   - Start the application using the appropriate command (e.g., `npm dev`).

### Note on Dockerization

The plan was to dockerize the application for easier deployment, but due to time constraints, this was not completed. Each service has its own deployment instructions, and you need to manually set up the environment variables as described above.

## Usage

- **Uploading Files**: Use the Node application's UI to upload files. These requests will be forwarded to the Python service, which will handle the file processing and data management.
- **Chat Functions**: The Node application manages chat functions, interfacing with the Python service for backend logic.

