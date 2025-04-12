from flask import Flask, render_template_string
from flask_socketio import SocketIO
import serial
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Traffic Sign System</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .alert { padding: 15px; margin: 10px 0; border-radius: 5px; }
        .speed { background-color: #FFEBEE; border-left: 5px solid #F44336; }
        .noise { background-color: #E3F2FD; border-left: 5px solid #2196F3; }
        .unknown { background-color: #FFF9C4; border-left: 5px solid #FFC107; }
        #log { margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
</head>
<body>
    <h1>Traffic Sign Detection System</h1>
    <div id="alerts"></div>
    <div id="log"></div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();
        
        socket.on('arduino_message', function(data) {
            const logDiv = document.getElementById('log');
            const entry = document.createElement('div');
            entry.textContent = data;
            logDiv.appendChild(entry);
            
            if (data.startsWith('ALERT_TYPE:')) {
                const alertType = data.split(':')[1];
                const alertsDiv = document.getElementById('alerts');
                const alert = document.createElement('div');
                
                if (alertType === 'speed_breaker') {
                    alert.className = 'alert speed';
                    alert.innerHTML = '<strong>Speed Breaker Detected</strong><p>Motor speed reduced to 75%</p>';
                } else if (alertType === 'noise_pollution') {
                    alert.className = 'alert noise';
                    alert.innerHTML = '<strong>Noise Pollution Area</strong><p>Horn volume reduced by 50%</p>';
                } else {
                    alert.className = 'alert unknown';
                    alert.innerHTML = '<strong>Unknown Tag Scanned</strong>';
                }
                
                alertsDiv.prepend(alert);
            }
        });
    </script>
</body>
</html>
"""

def read_serial():
    ser = serial.Serial('COM3', 115200, timeout=1)  # Update with your port
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                socketio.emit('arduino_message', line)
        except Exception as e:
            print(f"Serial error: {e}")
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    threading.Thread(target=read_serial, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)