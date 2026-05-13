from flask import Blueprint, Flask, render_template, request, redirect, session, url_for
import pymysql
from dotenv import load_dotenv
from libraries.crud import crud_bp
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'rotc_secret_key'

app.register_blueprint(crud_bp)

# DATABASE CONFIG
db_config = {
    'host': os.getenv("DB_SERVER"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE"),
    'cursorclass': pymysql.cursors.DictCursor
}


db_config2 = {
    'host': os.getenv("DB_SERVER"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE"),
    'cursorclass': pymysql.cursors.Cursor
}

def get_db():
    return pymysql.connect(**db_config)

def connect_db():
    return pymysql.connect(
        **db_config2
    )

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
        
            cursor.execute("SELECT * FROM team_members")
            members = cursor.fetchall()

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

    member_connect = connect_db()
    currr = member_connect.cursor()
    currr.execute("SELECT * FROM team_members")
    members = currr.fetchall()

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

        cursor.execute("""
            SELECT status, COUNT(*) AS count
            FROM equipment
            GROUP BY status
        """)
        equipment_status_stats = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        attendance_stats=attendance_stats,
        equipment_stats=equipment_stats,
        total_attendance=total_attendance,
        total_equipment=total_equipment,
        members=members,
        equipment_status_stats=equipment_status_stats
    )

# =========================
# ATTENDANCE
# =========================

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
    app.run(debug=True, port=5002)
