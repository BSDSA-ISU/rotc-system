from flask import Flask, render_template, request, redirect, session, url_for
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'rotc_secret_key'

# DATABASE CONFIG
db_config = {
    'host': os.getenv("DB_SERVER"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE"),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**db_config)

# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db()

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )

            user = cursor.fetchone()

        conn.close()

        if user:
            session['user'] = user['username']
            return redirect(url_for('dashboard'))

    return render_template('login.html')

# =========================
# DASHBOARD
# =========================

@app.route('/')
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT status, COUNT(*) AS count
            FROM attendance
            GROUP BY status
        """)
        attendance_stats = cursor.fetchall()

        cursor.execute("""
            SELECT item, SUM(quantity) AS total
            FROM equipment
            GROUP BY item
        """)
        equipment_stats = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM attendance")
        total_attendance = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM equipment")
        total_equipment = cursor.fetchone()['total']

    conn.close()

    return render_template(
        'dashboard.html',
        attendance_stats=attendance_stats,
        equipment_stats=equipment_stats,
        total_attendance=total_attendance,
        total_equipment=total_equipment
    )

# =========================
# ATTENDANCE
# =========================

@app.route('/attendance')
def attendance():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM attendance")
        records = cursor.fetchall()

    conn.close()

    return render_template('attendance.html', records=records)

# =========================
# ADD ATTENDANCE
# =========================

@app.route('/add_attendance', methods=['POST'])
def add_attendance():

    conn = get_db()

    with conn.cursor() as cursor:

        cursor.execute("""
            INSERT INTO attendance
            (name, rank, platoon, status, date_recorded, submitted_by)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            request.form['name'],
            request.form['rank'],
            request.form['platoon'],
            request.form['status'],
            request.form['date'],
            session['user']
        ))

    conn.commit()
    conn.close()

    return redirect(url_for('attendance'))

# =========================
# EQUIPMENT
# =========================

@app.route('/equipment')
def equipment():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM equipment")
        records = cursor.fetchall()

    conn.close()

    return render_template('equipment.html', records=records)

# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)