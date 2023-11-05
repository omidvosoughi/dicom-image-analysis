# DICOM Image Upload Application

This application provides a simple web interface to upload DICOM images, calculate thresholded pixel volume, and visualize them. The frontend is built with Vue.js, and the backend API is powered by FastAPI.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Git on your system.
- You have installed Docker and Docker Compose.

## Project Structure

- `/frontend`: This directory contains the Vue.js application.
- `/backend`: This directory contains the FastAPI application.
- `docker-compose.yml`: This file defines the multi-container Docker application.

## Running the Application

To get the application up and running, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/omidvosoughi/dicom-uploader.git
cd dicom-uploader
```

### 2. Build and Run with Docker Compose

Use 'docker-compose' to build and run both the frontend and backend services.

```bash
sudo docker-compose up --build
```

This command will build the images if they don't exist and start the containers. The '--build' option ensures that the latest versions of the applications are built and used.

### 3. Accessing the Application

After the containers are up and running, you can access the application in your web browser via following link.

- [http://localhost](http://localhost)

### 4. Upload DICOM Images

Go to the above link and upload DICOM images using the provided dropzone. The uploaded images will be processed by the backend, and the calculated volume and image visualization will be displayed.

