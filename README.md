# Wedding Photo Gallery Web App

This web application provides a photo gallery for a wedding website, where users can view and download wedding photos hosted in a Yandex Cloud S3-compatible bucket. Built with Flask and Boto3, it allows for easy management and display of images, supporting features like pagination and file downloading.

## Features

- **Wedding Photo Gallery**: Displays images from a Yandex Cloud S3 bucket in a gallery view.
- **File Pagination**: Efficiently loads images with pagination to avoid long load times.
- **Image Download**: Users can download images directly from the gallery.
- **Customizable Configurations**: Easily configure the application using environment variables for access keys and bucket information.
- **Error Handling**: Graceful error handling for missing files and configurations.


## Requirements

- Python 3.7+
- `Flask` - Web framework
- `Boto3` - AWS SDK for Python, used to interact with Yandex Cloud S3 storage
- `python-dotenv` (optional) - For loading environment variables from a `.env` file

## Setup

### 1. Clone the Repository

```bash
git clone https://your-repository-url.git
cd your-repository
```

### 2. Install Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a .env file or set the following environment variables manually:

```bash
YANDEX_BUCKET_NAME=your-bucket-name
YANDEX_ENDPOINT=https://storage.yandexcloud.net
YANDEX_ACCESS_KEY=your-access-key
YANDEX_SECRET_KEY=your-secret-key
SECRET_KEY=your-flask-secret-key
DEBUG=True
```

- YANDEX_BUCKET_NAME: Your Yandex Cloud S3 bucket name where images are stored.
- YANDEX_ACCESS_KEY: Your Yandex Cloud access key.
- YANDEX_SECRET_KEY: Your Yandex Cloud secret key.
- YANDEX_ENDPOINT: The endpoint URL for Yandex Cloud S3 (use the default https://storage.yandexcloud.net).
- SECRET_KEY: Flask’s secret key for signing cookies and sessions.
- DEBUG: Enable or disable Flask debug mode (set to True for development).

### 4. Run the Application

To start the application, run:

```bash
python run.py
```

By default, the application will be hosted on http://localhost:5000.

### 5. Docker Setup (Optional)

If you prefer running the application in a Docker container, you can build and run it with Docker:

```bash
docker build -t gallery .
docker run -p 5000:5000 gallery
```

## Routes

### /

Renders the main gallery page where users can view the images.

### /api/photos

Fetches a list of image files from the Yandex Cloud S3 bucket with optional pagination support. The response includes a list of files and the total number of files in the bucket.

### /download/<filename>

Allows users to download a file from the S3 bucket by clicking the file in the gallery.

### /favicon.ico

Serves the favicon for the web application.

### /robots.txt

Provides the robots.txt file for search engine crawlers.
