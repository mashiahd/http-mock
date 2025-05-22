#!flask/bin/python
from functools import wraps
import logging
import os
from pathlib import Path
import sys

from flask import Flask, make_response, request
from flask_compress import Compress
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging first
logging.basicConfig(
  filename='app.log',
  filemode='a',
  level=logging.ERROR,
  format='%(asctime)s [%(levelname)s] %(message)s'
)

# Default configuration
DEFAULT_CONFIG = {
  'HOST': '127.0.0.1',
  'PORT': '8080',
  'CONSOLE_PRINT': '0'
}

def create_default_env():
  env_path = Path('.env')
  if not env_path.exists():
    with open(env_path, 'w', encoding='utf-8') as f:
      for key, value in DEFAULT_CONFIG.items():
        f.write(f"{key}={value}\n")
    logging.error("Default .env file created. Please edit it with your desired values and run the application again.")
    sys.exit(0)

def load_config():
  create_default_env() # Create .env file if it doesn't exist
  
  # Load environment variables
  host = os.getenv('HOST', DEFAULT_CONFIG['HOST'])
  port = os.getenv('PORT', DEFAULT_CONFIG['PORT'])
  console_print = os.getenv('CONSOLE_PRINT', DEFAULT_CONFIG['CONSOLE_PRINT'])

  # Validate host
  if not host:
    logging.error("Error: HOST is not set in .env file")
    sys.exit(1)
  else:
    if not all(octet.isdigit() and 0 <= int(octet) <= 255 for octet in host.split('.')) or len(host.split('.')) != 4:
      logging.error("Error: HOST must be a valid IP address with 4 octets (e.g. 192.168.1.1)")
      sys.exit(1)
  
  # Validate port
  try:
    port = int(port)
    if not (1 <= port <= 65535):
      raise ValueError("Port must be between 1 and 65535")
  except ValueError as e:
    logging.error("Error in .env file: %s", e)
    sys.exit(1)
  
  return host, port, console_print

# Load configuration
config_host, config_port, config_console_print = load_config()

app = Flask(__name__)
app.config["DEBUG"] = False  # Disable debug mode in production
app.config["COMPRESS_MIMETYPES"] = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
app.config["COMPRESS_LEVEL"] = 6
app.config["COMPRESS_MIN_SIZE"] = 500

# Initialize compression
Compress(app)

# Configure logging
logging.basicConfig(
  filename='app.log',
  filemode='a',
  level=logging.ERROR,
  format='%(asctime)s [%(levelname)s] %(message)s'
)

# Set werkzeug logger to ERROR level to reduce noise
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# Set Flask logger to ERROR level
app.logger.setLevel(logging.ERROR)

def add_response_headers(headers={}):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      resp = make_response(f(*args, **kwargs))
      h = resp.headers
      for header, value in headers.items():
        h[header] = value
      return resp
    return decorated_function
  return decorator

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@add_response_headers({
  'Cache-Control': 'no-cache, no-store, must-revalidate',
  'Pragma': 'no-cache',
  'Expires': '0'
})
def catch_all(path):
  app.logger.info('Request received: %s %s', request.method, path)
  if config_console_print == '1':
    print(f"Request received: {request.method} {path}")
  return '', 204

@app.route('/monitors/isalive', methods=['GET'])
@add_response_headers({
  'Cache-Control': 'no-cache, no-store, must-revalidate',
  'Pragma': 'no-cache',
  'Expires': '0'
})
def hc():
  return "up", 200

if __name__ == "__main__":
  print(f"Host: {config_host}, Port: {config_port}")
  app.run(host=config_host, port=config_port)
