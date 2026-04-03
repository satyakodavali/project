from flask import Flask, jsonify
from flask_cors import CORS
from flask_session import Session
from config import Config
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp
from routes.chatbot_routes import chatbot_bp

app = Flask(__name__)
app.config.from_object(Config)

# Proper CORS for sessions
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"])

Session(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(student_bp, url_prefix='/api/student')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "NSRIT Portal API is running"})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
