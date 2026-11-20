from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

DB = "phishcapture.db"


def init_db():
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            timestamp TEXT,
            password_captured TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/simulate", methods=["POST"])
def simulate():

    email = request.form.get("email", "").strip()

    if not email or len(email) > 254:
        return "Invalid demo email", 400
        
    password = request.form.get("password_captured", "").strip()

    if not password or len(password) > 254:
        return "Invalid demo password", 400
        

    conn = sqlite3.connect(DB)

    conn.execute(
        "INSERT INTO attempts (email, timestamp, password_captured) VALUES (?, ?, ?)",
        (email, datetime.now().isoformat(), password)
    )

    conn.commit()
    conn.close()

    return render_template("login.html", message="Simulation complete.")


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DB)

    records = conn.execute(
        "SELECT id, email, timestamp, password_captured FROM attempts ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        records=records
    )


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
