from flask import Blueprint, request, jsonify, session
from chatbot.engine import process_query
from utils.db import get_db_connection
from utils.sms import send_sms
from utils.email_service import send_email_otp

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'status': 'error', 'message': 'No query provided'}), 400
        
    user_query = data['query']
    is_guest_mode = data.get('is_guest_mode', False)
    
    # If in guest mode (Home page), only allow if already verified as parent
    # Otherwise, ignore any student session to avoid "last logged in" state
    if is_guest_mode and session.get('role') != 'parent':
        user_context = {
            'role': 'guest',
            'roll_no': None,
            'name': 'Guest'
        }
    else:
        # Normal authenticated context (parent or student on their respective pages)
        user_context = {
            'role': session.get('role'),
            'roll_no': session.get('roll_no'),
            'name': session.get('name')
        }
    
    response = process_query(user_query, user_context)
    
    return jsonify({
        'status': 'success',
        'response': response
    })

@chatbot_bp.route('/ask', methods=['POST'])
def handle_ask():
    data = request.json
    if not data or 'question' not in data:
        return jsonify({'status': 'error', 'message': 'No question provided'}), 400
        
    question = data['question']
    is_guest_mode = data.get('is_guest_mode', False)
    
    if is_guest_mode and session.get('role') != 'parent':
        user_context = {
            'role': 'guest',
            'roll_no': None,
            'name': 'Guest'
        }
    else:
        role = session.get('role', 'student')
        roll_no = session.get('roll_no')
        
        if not roll_no:
            return jsonify({'status': 'error', 'message': 'User not logged in'}), 401
            
        user_context = {
            'role': role,
            'roll_no': roll_no,
            'name': session.get('name')
        }
    
    response = process_query(question, user_context)
    
    return jsonify({
        'status': 'success',
        'response': response
    })

@chatbot_bp.route('/parent/request-otp', methods=['POST'])
def request_parent_otp():
    data = request.json
    if not data or 'roll_no' not in data:
        return jsonify({'status': 'error', 'message': 'Roll number required'}), 400
        
    roll_no = data['roll_no'].strip().upper()

    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
        
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT name, parents_email FROM students WHERE UPPER(roll_no) = UPPER(?)",
            (roll_no,)
        )
        student = cursor.fetchone()

        if not student:
            return jsonify({'status': 'error', 'message': 'Invalid Roll Number'}), 404

        parent_email = student['parents_email']

        if not parent_email:
            return jsonify({'status': 'error', 'message': 'No parent email registered'}), 400

        # 🔥 Generate OTP
        import random
        otp = str(random.randint(100000, 999999))

        # 🔥 Store session
        import time
        session['parent_otp'] = otp
        session['parent_roll_no'] = roll_no
        session['student_name'] = student['name']
        session['otp_time'] = time.time()

        # 🔥 SEND EMAIL
        email_sent = send_email_otp(parent_email, otp, student['name'])

        if not email_sent:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send OTP. Check email config.'
            }), 500

        print(f"[EMAIL LOG] OTP successfully sent to {parent_email}")

        # 🔥 Mask email
        name_part, domain = parent_email.split('@')
        masked_email = name_part[0] + "***@" + domain

        return jsonify({
            'status': 'success',
            'message': f'OTP sent to {masked_email}',
            'email': masked_email
        })

    finally:
        cursor.close()
        conn.close()

@chatbot_bp.route('/parent/verify-otp', methods=['POST'])
def verify_parent_otp():
    data = request.json

    if not data or 'otp' not in data or 'roll_no' not in data:
        return jsonify({'status': 'error', 'message': 'OTP and roll number required'}), 400

    otp = data['otp'].strip()
    roll_no = data['roll_no'].strip().upper()

    import time
    otp_time = session.get('otp_time', 0)

    # ⏳ Expiry check (5 minutes)
    if time.time() - otp_time > 300:
        return jsonify({'status': 'error', 'message': 'OTP expired'}), 401

    if session.get('parent_otp') == otp and session.get('parent_roll_no') == roll_no:

        # ✅ Login success
        session['roll_no'] = roll_no
        session['name'] = f"Parent of {session.get('student_name')}"
        session['role'] = 'parent'

        # 🔥 Clear OTP
        session.pop('parent_otp', None)
        session.pop('parent_roll_no', None)
        session.pop('otp_time', None)

        return jsonify({
            'status': 'success',
            'message': 'OTP verified successfully',
            'name': session['name']
        })

    return jsonify({'status': 'error', 'message': 'Invalid OTP'}), 401
    
@chatbot_bp.route('/parent/get-last-otp', methods=['GET'])
def get_last_otp():
    """DIAGNOSTIC ROUTE: Used only for automated testing to retrieve the last generated OTP."""
    otp = session.get('parent_otp')
    roll = session.get('parent_roll_no')
    if otp:
        return jsonify({'status': 'success', 'otp': otp, 'roll_no': roll})
    return jsonify({'status': 'error', 'message': 'No OTP currently in session'}), 404