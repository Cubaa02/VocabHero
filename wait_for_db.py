# wait_for_db.py
import os
import time
import sys
import socket
import urllib.parse

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # fallback to individual vars
    DB_HOST = os.environ.get("POSTGRES_HOST", "db")
    DB_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
else:
    # parse DATABASE_URL like postgres://user:pass@host:port/dbname
    parsed = urllib.parse.urlparse(DATABASE_URL)
    DB_HOST = parsed.hostname or "db"
    DB_PORT = parsed.port or 5432

RETRIES = 20
SLEEP = 2

for i in range(RETRIES):
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=5):
            print(f"DB {DB_HOST}:{DB_PORT} dostupná")
            sys.exit(0)
    except Exception as e:
        print(f"Čekám na DB ({i+1}/{RETRIES})... - {e}")
        time.sleep(SLEEP)

print("DB se neprobudila včas, končím.")
sys.exit(1)
