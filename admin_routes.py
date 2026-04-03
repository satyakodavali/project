from flask import Blueprint, request, jsonify, session
from utils.db import get_db_connection
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return jsonify({'status': 'error', 'message': 'Unauthorized: Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/students', methods=['GET'])
@admin_required
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT roll_no, name, branch, section, year FROM students ORDER BY roll_no LIMIT 100")
        students = cursor.fetchall()
        return jsonify({'status': 'success', 'data': students})
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/student', methods=['POST'])
@admin_required
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Straight storage for 8-char password as per user policy
        password = data['password']
        cursor.execute("""
            INSERT INTO students (roll_no, name, branch, section, year, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (data['roll_no'], data['name'], data['branch'], data['section'], data['year'], password))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Student added successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/student/<roll_no>', methods=['DELETE'])
@admin_required
def delete_student(roll_no):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'status': 'success', 'message': 'Student deleted successfully'})
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        cursor.close()
        conn.close()
