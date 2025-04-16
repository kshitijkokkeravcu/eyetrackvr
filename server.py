from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import sys
import os
import csv
import time
import argparse
from eye_data import EyeData  # Import the EyeData class

parser = argparse.ArgumentParser(description="Arguments for server.")
parser.add_argument("-i","--ip", help="ip addr of the eyetrackvr", default="127.0.0.1")
parser.add_argument("-p","--port", help="port number of the eyetrackvr osc client", default=9000)
args = parser.parse_args()

# Dictionary to store received OSC messages
message = {}

# Initialize EyeData object to store eye tracking data
eye_data = EyeData()

# For in-place printing
def print_eye_data():
    """Print eye data in a clean, visually appealing format with raw values"""
    # Get values
    eyes_y = eye_data.get_eyes_y()
    left_lid = eye_data.get_left_eye_lid()
    left_squeeze = eye_data.get_left_eye_lid_expanded_squeeze()
    left_x = eye_data.get_left_eye_x()
    right_lid = eye_data.get_right_eye_lid()
    right_squeeze = eye_data.get_right_eye_lid_expanded_squeeze()
    right_x = eye_data.get_right_eye_x()
    
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print header
    print(f"╔═══════════════════════════════════════════════════════════════╗")
    print(f"║             EyeTrackVR OSC Data Monitor                       ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    print(f"║ Listening on {ip}:{port}                                   ║")
    print(f"║ Press Ctrl+C to exit                                          ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    
    # Raw eye position values
    print(f"║ Eye Y:    {eyes_y:<51} ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    
    # Left Eye values
    print(f"║ LEFT EYE:                                                     ║")
    print(f"║   X Pos:  {left_x:<51} ║")
    print(f"║   Lid:    {left_lid:<51} ║")
    print(f"║   Squeeze:{left_squeeze:<51} ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    
    # Right Eye values
    print(f"║ RIGHT EYE:                                                    ║")
    print(f"║   X Pos:  {right_x:<51} ║")
    print(f"║   Lid:    {right_lid:<51} ║")
    print(f"║   Squeeze:{right_squeeze:<51} ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    
    # Time
    current_time = eye_data.get_timestamp().strftime('%H:%M:%S') if eye_data.get_timestamp() else ''
    print(f"║ Last Update: {current_time:<49}║")
    print(f"╚═══════════════════════════════════════════════════════════════╝")
    
    # Flush stdout to ensure immediate display
    sys.stdout.flush()

last_time = time.time()
def default_handler(address, *args):
    """Handles all other OSC messages."""
    global last_time, message
    
    # Store the message
    message[address] = args
    
    # Update the eye_data object as soon as we receive any message
    eye_data.update_from_osc_message({address: args})
    
    if len(message) == 7:
        # Write to CSV and update display if 1 second has passed
        wait_time = 1.0
        if time.time() - last_time >= wait_time:
            last_time = time.time()
            
            # Print updated eye data in place
            print_eye_data()
            
            # Write to CSV
            with open("osc_data.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                row = eye_data.to_csv_row()
                writer.writerow(row)

# --- Setup ---
headers = [
    '/avatar/parameters/EyesY',
    '/avatar/parameters/LeftEyeLid',
    '/avatar/parameters/LeftEyeLidExpandedSqueeze',
    '/avatar/parameters/LeftEyeX',
    '/avatar/parameters/RightEyeLid',
    '/avatar/parameters/RightEyeLidExpandedSqueeze',
    '/avatar/parameters/RightEyeX',
    "time"
]

# Initialize CSV file with headers
with open("osc_data.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)  # Write specified header row

# Setup OSC dispatcher
dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

ip = args.ip
port = int(args.port)  # Ensure port is an integer

# Initial screen setup
os.system('cls' if os.name == 'nt' else 'clear')
print(f"Listening for OSC messages on {ip}:{port}...")
print("Press Ctrl+C to exit.")
print("\nWaiting for eye tracking data...")
sys.stdout.flush()

# Start the server
server = BlockingOSCUDPServer((ip, port), dispatcher)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
    sys.exit(0)