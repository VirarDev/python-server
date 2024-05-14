import subprocess
import os
import sys

from flask import Flask, jsonify, render_template

# Import FastAPI and related dependencies
from fastapi import FastAPI
from flask import jsonify, render_template
from uvicorn import Config, Server

# Specify the new working directory path
SERVER_working_directory = os.path.join(os.getcwd(), "MAIN")
os.chdir(SERVER_working_directory)
print(os.getcwd())

# Initialize FastAPI app
app = Flask(__name__)

# Shared memory for process management
sys.SharedMemory = {}
sys.SharedMemory["process"] = None
sys.SharedMemory["is_process_running"] = False

# Function to execute shell commands
def exe(cmd):
    subprocess.Popen(cmd, shell=True)

# Function to start the FastAPI server
def start_server():
    if sys.SharedMemory["is_process_running"]:
        print("Already a process is running")
        return False
    try:
        exe("uvicorn vellore:app --host 0.0.0.0 --port 50088 --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")
        exe("uvicorn virar:app --host 0.0.0.0 --port 50087 --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")
        exe("uvicorn talentov:app --host 0.0.0.0 --port 5000 --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")
        sys.SharedMemory["is_process_running"] = True
        return True
    except Exception as e:
        print(f"Error starting FastAPI app: {e}")
        return False

# Function to stop the FastAPI server
def stop_server():
    try:
        exe("sudo pkill -f 'uvicorn.*vellore:app'")
        exe("sudo pkill -f 'uvicorn.*virar:app'")
        exe("sudo pkill -f 'uvicorn.*talentov:app'")
    except:
        pass
    if sys.SharedMemory["is_process_running"]:
        try:
            sys.SharedMemory["is_process_running"] = False
            return True
        except Exception as e:
            print(f"Error stopping FastAPI app: {e}")
            return False
    else:
        return False

# Flask routes
@app.route('/start', methods=['GET'])
def start_fastapi_app():
    if sys.SharedMemory["process"] is None or sys.SharedMemory["process"].poll() is not None:
        return jsonify({"status": start_server()})
    else:
        return jsonify({"status": "FastAPI app is already running."})

@app.route('/stop', methods=['GET'])
def stop_fastapi_app():
    return jsonify({"status": stop_server()})

@app.route('/restart', methods=['GET'])
def restart_server():
    log = ""
    try:
        if stop_server():
            log += "Stopped,"
        else:
            log += "Not In Run,"
        if start_server():
            log += "Started"
        else:
            log += "Failed To Start"
        return jsonify({"status": log})
    except:
        return jsonify({"status": "Error log: " + log})

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
