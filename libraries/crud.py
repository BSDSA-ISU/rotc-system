from flask import Blueprint, render_template, request, redirect, session, url_for
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

crud_bp = Blueprint('crud', __name__)

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
# ATTENDANCE PAGE
# =========================

@crud_bp.route('/attendance')
def attendance():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()

    edit_record = None

    with conn.cursor() as cursor:

        cursor.execute("SELECT * FROM attendance")
        records = cursor.fetchall()

        edit_id = request.args.get('edit')

        if edit_id:

            cursor.execute(
                "SELECT * FROM attendance WHERE id=%s",
                (edit_id,)
            )

            edit_record = cursor.fetchone()

    conn.close()

    return render_template(
        'attendance.html',
        records=records,
        edit_record=edit_record
    )
# =========================
# ADD ATTENDANCE
# =========================

@crud_bp.route('/add_attendance', methods=['POST'])
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

    return redirect(url_for('crud.attendance'))

# =========================
# DELETE ATTENDANCE
# =========================

@crud_bp.route('/delete_attendance/<int:id>')
def delete_attendance(id):

    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM attendance WHERE id=%s",
            (id,)
        )

    conn.commit()
    conn.close()

    return redirect(url_for('crud.attendance'))

# =========================
# EDIT ATTENDANCE
# =========================

@crud_bp.route('/edit_attendance/<int:id>', methods=['GET', 'POST'])
def edit_attendance(id):

    conn = get_db()

    if request.method == 'POST':

        with conn.cursor() as cursor:

            cursor.execute("""
                UPDATE attendance
                SET
                    name=%s,
                    rank=%s,
                    platoon=%s,
                    status=%s,
                    date_recorded=%s
                WHERE id=%s
            """, (
                request.form['name'],
                request.form['rank'],
                request.form['platoon'],
                request.form['status'],
                request.form['date'],
                id
            ))

        conn.commit()
        conn.close()

        return redirect(url_for('crud.attendance'))

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM attendance WHERE id=%s",
            (id,)
        )

        record = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_attendance.html',
        record=record
    )

# =========================
# EQUIPMENT PAGE
# =========================

@crud_bp.route('/equipment')
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
# ADD EQUIPMENT
# =========================

@crud_bp.route('/add_equipment', methods=['POST'])
def add_equipment():

    conn = get_db()

    with conn.cursor() as cursor:

        cursor.execute("""
            INSERT INTO equipment
            (borrower, item, quantity, borrow_date, status, submitted_by)
            VALUES (%s,%s,%s,%s,'Borrowed',%s)
        """, (
            request.form['borrowerName'],
            request.form['equipment'],
            request.form['quantity'],
            request.form['borrowDate'],
            session['user']
        ))

    conn.commit()
    conn.close()

    return redirect(url_for('equipment'))

# =========================
# DELETE EQUIPMENT
# =========================

@crud_bp.route('/delete_equipment/<int:id>')
def delete_equipment(id):

    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM equipment WHERE id=%s",
            (id,)
        )

    conn.commit()
    conn.close()

    return redirect(url_for('crud.equipment'))

# =========================
# EDIT EQUIPMENT
# =========================

@crud_bp.route('/edit_equipment/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):

    conn = get_db()

    if request.method == 'POST':

        with conn.cursor() as cursor:

            cursor.execute("""
                UPDATE equipment
                SET
                    borrower=%s,
                    item=%s,
                    quantity=%s,
                    borrow_date=%s
                WHERE id=%s
            """, (
                request.form['borrower'],
                request.form['item'],
                request.form['quantity'],
                request.form['borrow_date'],
                id
            ))

        conn.commit()
        conn.close()

        return redirect(url_for('crud.equipment'))

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM equipment WHERE id=%s",
            (id,)
        )

        record = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_equipment.html',
        record=record
    )

@crud_bp.route('/return_equipment/<int:id>')
def return_equipment(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE equipment
            SET status = 'Returned',
                return_date = CURDATE()
            WHERE id = %s
        """, (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('equipment'))