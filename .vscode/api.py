# api.py
from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

SESSION_FILE = "user_sessions.json"

def load_sessions():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    with open(SESSION_FILE, 'w') as f:
        json.dump(sessions, f)

user_sessions = load_sessions()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    login_time = datetime.now().isoformat()
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {'login_time': login_time, 'logout_time': None, 'total_time': 0}
    else:
        user_sessions[user_id]['login_time'] = login_time
    
    save_sessions(user_sessions)  # Save sessions to file
    return jsonify({"message": "Login time recorded", "data": user_sessions[user_id]}), 200

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    user_id = data.get('user_id')
    logout_time = datetime.now().isoformat()
    
    if user_id in user_sessions:
        user_sessions[user_id]['logout_time'] = logout_time
        login_time = datetime.fromisoformat(user_sessions[user_id]['login_time'])
        logout_time_dt = datetime.fromisoformat(logout_time)
        total_time = (logout_time_dt - login_time).total_seconds()
        user_sessions[user_id]['total_time'] += total_time
    
    save_sessions(user_sessions)  # Save sessions to file
    return jsonify({"message": "Logout time recorded", "data": user_sessions[user_id]}), 200

@app.route('/sessions', methods=['GET'])
def get_sessions():
    return jsonify(user_sessions), 200

if __name__ == "__main__":
    app.run(port=5000)