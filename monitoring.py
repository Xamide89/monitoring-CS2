from fastapi import FastAPI
from pydantic import BaseModel
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Metric(BaseModel):
    host: str
    cpu: float
    ram: float
    disk: float

def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    return conn

@app.post("/metrics")
def receive_metrics(metric: Metric):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO metrics (host, cpu, ram, disk)
        VALUES (?, ?, ?, ?)
    """, metric.host, metric.cpu, metric.ram, metric.disk)

    conn.commit()
    conn.close()

    return {"status": "stored"}

@app.get("/metrics")
def get_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM metrics")
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append({
            "host": r[0],
            "cpu": r[1],
            "ram": r[2],
            "disk": r[3]
        })

    conn.close()
    return result
