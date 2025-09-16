from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "testdb"),
            user=os.getenv("POSTGRES_USER", "user"),
            password=os.getenv("POSTGRES_PASSWORD", "pass"),
            host="db"
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        conn.close()
        return f"📦 Hola desde Flask! Hora en DB: {result[0]}"
    except Exception as e:
        return f"Error conectando a DB: {e}"

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 5000))