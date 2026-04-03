from flask import Blueprint, request, jsonify, session
import re
from utils.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

def is_valid_password(pwd):
    # Requirement: Secure passwords. Standardizing on 8+ chars for security.
    if len(pwd) < 8: return False
    if not re.search(r'[A-Z]', pwd): return False
    if not re.search(r'[^a-zA-Z0-9]', pwd): return False
    return True

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400
        
    username = data.get('username')
    password = data.get('password')
    type = data.get('type', 'student') 
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
        
    cursor = conn.cursor()
    
    try:
        if type == 'admin':
            cursor.execute("SELECT id, username, password_hash FROM admins WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session['admin_id'] = user['id']
                session['username'] = user['username']
                session['role'] = 'admin'
                return jsonify({'status': 'success', 'message': 'Admin login successful', 'role': 'admin'})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid admin credentials'}), 401
                
        else: # Student 
            cursor.execute("SELECT roll_no, name, password_hash FROM students WHERE UPPER(roll_no) = UPPER(?)", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session['roll_no'] = user['roll_no']
                session['name'] = user['name']
                session['role'] = 'student'
                return jsonify({'status': 'success', 'message': 'Student login successful', 'role': 'student', 'name': user['name'], 'roll_no': user['roll_no']})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid student credentials'}), 401
                
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    required_fields = ['roll_no', 'name', 'branch', 'password']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
    roll_no = data['roll_no']
    name = data['name']
    branch = data['branch']
    password = data['password']
    
    if not is_valid_password(password):
        return jsonify({'status': 'error', 'message': 'Password must be at least 8 characters with 1 uppercase and 1 special char'}), 400
    
    hashed_pw = generate_password_hash(password)
    section = data.get('section', 'A')
    year = data.get('year', 1)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT roll_no FROM students WHERE roll_no = ?", (roll_no,))
        if cursor.fetchone():
            return jsonify({'status': 'error', 'message': 'Student exists'}), 409
            
        cursor.execute("""
            INSERT INTO students (roll_no, name, branch, section, year, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roll_no, name, branch, section, year, hashed_pw))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Registration successful'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    if 'role' not in session or session['role'] != 'student':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
    data = request.json
    roll_no = session['roll_no']
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not is_valid_password(new_password):
        return jsonify({'status': 'error', 'message': 'Invalid new password format'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT password_hash FROM students WHERE roll_no = ?", (roll_no,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], old_password):
            return jsonify({'status': 'error', 'message': 'Invalid old password'}), 401
            
        hashed_new = generate_password_hash(new_password)
        cursor.execute("UPDATE students SET password_hash = ? WHERE roll_no = ?", (hashed_new, roll_no))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Password changed successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'role' in session:
        result = {'status': 'success', 'role': session['role']}
        if session['role'] == 'student':
            result['roll_no'] = session.get('roll_no')
            result['name'] = session.get('name')
        elif session['role'] == 'admin':
            result['username'] = session.get('username')
        return jsonify(result)
    return jsonify({'status': 'error', 'message': 'No active session'}), 401
