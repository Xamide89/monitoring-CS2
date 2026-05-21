from fastapi import FastAPI, Request
from pydantic import BaseModel
import pyodbc
import os
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(
    directory="templates"
)

load_dotenv()

app = FastAPI()

HOST_MAP = {
    "student": "Monitoring Server",
    "FS01": "File Server",
    "WIN-2H75UQOM7PG": "Domain Controller"
}

class Metric(BaseModel):
    host: str
    cpu: float
    ram: float
    disk: float

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        WITH latest AS (

        SELECT *,
            ROW_NUMBER() OVER (
                PARTITION BY host
                ORDER BY id DESC
            ) AS rn

        FROM metrics

    )

    SELECT host,cpu,ram,disk

    FROM latest

    WHERE rn=1
        """
    )

    rows = cursor.fetchall()

    metrics = []

    for r in rows:

        metrics.append({
            "host": r[0],
            "cpu": r[1],
            "ram": r[2],
            "disk": r[3]
        })

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "metrics": metrics
        }
    )

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
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO metrics (host, cpu, ram, disk)
            VALUES (?, ?, ?, ?)
        """, metric.host, metric.cpu, metric.ram, metric.disk)

        conn.commit()
        conn.close()

        return {"status": "stored"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/metrics")
def get_metrics():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""SELECT host, cpu, ram, disk FROM metrics""")
        rows = cursor.fetchall()

        result = []
        for r in rows:
            host = HOST_MAP.get(
                r[0],
                r[0]
            )
            result.append({
                "host": host,
                "cpu": r[1],
                "ram": r[2],
                "disk": r[3]
            })

        conn.close()
        return result

    except Exception as e:
        return {"error": str(e)}
