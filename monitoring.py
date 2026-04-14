import psutil
import socket
import time
import json
import os

# можно потом заменить на .env
API_URL = os.getenv("API_URL", "http://localhost:8000/metrics")
INTERVAL = int(os.getenv("INTERVAL", 10))

def collect_metrics():
    return {
        "host": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "timestamp": time.time()
    }

def main():
    print(f"[INFO] Monitoring started. Sending to {API_URL}")
    
    while True:
        data = collect_metrics()
        print("[DATA]", json.dumps(data, indent=2))
        
        # пока без API — просто вывод
        # позже добавим requests.post(...)
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()