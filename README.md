Traffic Sign and Board Recognition System (TSBRS)
Overview :
The Traffic Sign and Board Recognition System (TSBRS) is an RFID-based solution designed to detect and alert drivers about specific traffic signs (speed breakers and noise pollution zones) in real-time. The system consists of an Arduino component for RFID tag detection and a Flask-based web interface for displaying alerts and managing penalties.

Features :
RFID Tag Detection: Recognizes pre-programmed RFID tags for speed breakers and noise pollution zones

Audible Alerts: Provides distinct beep patterns for different alert types

Web Interface: Real-time display of detected signs with visual and textual information

Penalty System: Tracks violations with monetary penalties

System Controls: Start/stop functionality with penalty summary

Hardware Requirements :
Arduino board (Uno, Nano, etc.)

MFRC522 RFID reader module

Buzzer for audible alerts

RFID tags (minimum 2 for testing)

Software Requirements
Arduino IDE (for uploading the firmware)

Python 3.7+

Required Python packages (listed in requirements.txt)

Installation
Arduino Setup
Connect the RFID reader to your Arduino:

SDA pin → Digital 10

SCK pin → Digital 13

MOSI pin → Digital 11

MISO pin → Digital 12

RST pin → Digital 9

Buzzer → Digital 6

Upload the traffic_system.ino sketch to your Arduino

Note the COM port where your Arduino is connected

Python Server Setup
Install required Python packages:

bash
pip install -r requirements.txt
Update the find_arduino_port() function in traffic_ui_server.py if your Arduino uses a different port

Run the server:

bash
python traffic_ui_server.py
Cloudflare Tunnel (Optional)
To expose your local server to the internet:

Install Cloudflare Tunnel

Update config.yml with your credentials

Run:

bash
cloudflared tunnel run
Usage
Power on the Arduino with connected RFID reader

Start the Python server

Open the web interface at http://localhost:5000

Click "Start System"

Scan RFID tags to simulate traffic sign detection

Customization
RFID Tags: Update the tag UIDs in traffic_system.ino to match your physical tags

Alert Types: Modify SIGN_TYPES in traffic_ui_server.py to add or change sign definitions

Penalty Amounts: Adjust penalty values in the SIGN_TYPES dictionary

File Structure
├── traffic_system.ino       # Arduino firmware for RFID detection
├── traffic_ui_server.py     # Flask web server with SocketIO
├── index.html               # Web interface
├── requirements.txt         # Python dependencies
├── config.yml               # Cloudflare tunnel configuration
└── README.md                # This file
Troubleshooting
No Arduino detected: Check COM port connections and update find_arduino_port()

RFID not reading: Verify wiring and tag UIDs match the programmed values

Web interface not updating: Ensure the server is running and check browser console for errors