# HTTP Mock Server

A lightweight, configurable HTTP mock server built with Flask that provides standardized responses to all incoming requests. Perfect for testing, development, and API simulation scenarios.

## Features

- 🚀 **Universal Request Handling**: Responds to all HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- 🔄 **Configurable Responses**: Customize response codes and headers
- 📝 **Request Logging**: Built-in logging system for request tracking
- 🔒 **Security Headers**: Automatic security headers for all responses
- 🗜️ **Response Compression**: Built-in compression support for efficient responses
- 🏥 **Health Check Endpoint**: Built-in `/monitors/isalive` endpoint for monitoring
- ⚙️ **Environment Configuration**: Easy configuration through `.env` file

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/http-mock.git
cd http-mock
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The server can be configured through a `.env` file. A default configuration will be created on first run with these settings:

```env
HOST=127.0.0.1
PORT=8080
CONSOLE_PRINT=1
RESPONSE_STATUS_CODE=204
```

## Usage

1. Start the server:
```bash
python app.py
```

2. The server will start on the configured host and port (default: http://127.0.0.1:8080)

3. Send requests to any endpoint:
```bash
# Example requests
curl http://localhost:8080/any/path
curl -X POST http://localhost:8080/api/test
curl -X PUT http://localhost:8080/resource/1
```

4. Check server health:
```bash
curl http://localhost:8080/monitors/isalive
```

## Response Details

- All requests receive a 204 No Content response by default
- Health check endpoint (`/monitors/isalive`) returns "up" with 200 status
- All responses include security headers:
  - Cache-Control: no-cache, no-store, must-revalidate
  - Pragma: no-cache
  - Expires: 0

## Development

The project uses:
- Python 3.x
- Flask for the web framework
- Flask-Compress for response compression
- python-dotenv for configuration management

## License

This project is licensed under the terms of the included LICENSE file.
