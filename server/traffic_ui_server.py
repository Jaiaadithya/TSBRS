import os
from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
import serial.tools.list_ports
import threading
import time

# Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

# Initialize Flask app
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
socketio = SocketIO(app)

# Sign definitions
SIGN_TYPES = {
    "SPEED_BREAKER": {
        "icon": "🛑",
        "title": "Speed Breaker Detected",
        "description": "Reduce speed to 30km/h",
        "penalty": 200
    },
    "NOISE_POLLUTION": {
        "icon": "🔇",
        "title": "Noise Pollution Zone",
        "description": "Horn volume reduced by 50%",
        "penalty": 300
    }
}

# Find the Arduino COM port
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'USB Serial Device' in port.description:
            return port.device
    return 'COM4'  # fallback

# Read from Serial Port
def read_serial():
    arduino_port = find_arduino_port()
    print(f"Connecting to Arduino on {arduino_port}")

    try:
        ser = serial.Serial(arduino_port, 115200, timeout=1)
        print("Successfully connected to Arduino")
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")
        return

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Received: {line}")

                if line.startswith("ALERT_TYPE:"):
                    alert_type = line.split(":")[1]
                    if alert_type in SIGN_TYPES:
                        socketio.emit('sign_detected', SIGN_TYPES[alert_type])
        except Exception as e:
            print(f"Serial error: {e}")
            time.sleep(1)
        time.sleep(0.1)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Start server
if __name__ == '__main__':
    threading.Thread(target=read_serial, daemon=True).start()
    print("Starting server on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
