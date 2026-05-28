import psutil
import socket
import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

def collect_metrics():
    return {
        "host": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent
    }

def send_metrics():

    data = collect_metrics()

    try:

        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )

        print(
            f"Sent metrics: "
            f"{response.status_code}"
        )

    except Exception as e:

        print(f"Error: {e}")

while True:

    send_metrics()

    time.sleep(60)
