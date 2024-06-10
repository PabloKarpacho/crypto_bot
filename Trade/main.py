import os

import uvicorn

from src.config import Config

# THIS FILE ONLY FOR DEV AND FOR DEBUGGING. Test and Prod run via Docker

# Service config
THIS_SERVICE_PATH = "0.0.0.0"
THIS_SERVICE_PORT = "9020"

os.environ['API_KEY'] = Config.api_key
os.environ['API_SECRET'] = Config.api_secret


def start():


    try:
        uvicorn.run(
            "src.service:app",
            host=THIS_SERVICE_PATH,
            port=int(THIS_SERVICE_PORT),
            reload=False)
    finally:
        print("stopping server:app...")


if __name__ == '__main__':
    start()