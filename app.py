import os
import time

import psutil
import psycopg2


def conectar():
    """Reintenta hasta que la base de datos acepte conexiones."""
    while True:
        try:
            conn = psycopg2.connect(
                host=os.environ["DB_HOST"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
            conn.autocommit = True
            return conn
        except psycopg2.OperationalError as e:
            print(f"BD no disponible, reintentando: {e}", flush=True)
            time.sleep(2)


def preparar(conn):
    """Crea la tabla si no existe y devuelve un cursor."""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metricas (
            id SERIAL PRIMARY KEY,
            momento TIMESTAMPTZ DEFAULT now(),
            cpu REAL,
            ram REAL,
            disco REAL
        )
    """)
    return cur


conn = conectar()
cur = preparar(conn)

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent

    try:
        cur.execute(
            "INSERT INTO metricas (cpu, ram, disco) VALUES (%s, %s, %s)",
            (cpu, ram, disco),
        )
        print(f"Guardado: CPU {cpu}% | RAM {ram}% | Disco {disco}%", flush=True)
    except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
        print(f"Conexión perdida: {e}", flush=True)
        try:
            conn.close()
        except Exception:
            pass
        conn = conectar()
        cur = preparar(conn)

    time.sleep(4)mport os
import time

import psutil
import psycopg2


def conectar():
    """Reintenta hasta que la base de datos acepte conexiones."""
    while True:
        try:
            return psycopg2.connect(
                host=os.environ["DB_HOST"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
        except psycopg2.OperationalError as e:
            print(f"BD no disponible, reintentando: {e}", flush=True)
            time.sleep(2)


conn = conectar()
conn.autocommit = True
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS metricas (
        id SERIAL PRIMARY KEY,
        momento TIMESTAMPTZ DEFAULT now(),
        cpu REAL,
        ram REAL,
        disco REAL
    )
""")

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent

    cur.execute(
        "INSERT INTO metricas (cpu, ram, disco) VALUES (%s, %s, %s)",
        (cpu, ram, disco),
    )
    print(f"Guardado: CPU {cpu}% | RAM {ram}% | Disco {disco}%", flush=True)
    time.sleep(4)
