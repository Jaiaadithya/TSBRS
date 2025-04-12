from flask import Flask, render_template  
from flask_socketio import SocketIO  
import serial  
import serial.tools.list_ports  
import threading  
import time  
import os  

app = Flask(__name__,  
             template_folder=os.path.abspath("../templates"),  
             static_folder=os.path.abspath("../static"))  
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

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'USB Serial Device' in port.description:
            return port.device
    return 'COM4'  # Fallback to COM4 if not found

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
                print(f"Received: {line}")  # Debug output
                
                if line.startswith("ALERT_TYPE:"):
                    alert_type = line.split(":")[1]
                    if alert_type in SIGN_TYPES:
                        socketio.emit('sign_detected', SIGN_TYPES[alert_type])
        except Exception as e:
            print(f"Serial error: {e}")
            time.sleep(1)
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start serial reader in background
    threading.Thread(target=read_serial, daemon=True).start()
    print("Starting server on http://localhost:5000")
    # Disable debug autoreload to prevent re-opening the COM port
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
