from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import sys
import pprint
import os
import csv
import datetime
import time
# List to store all received OSC messages
message = {}

def print_handler(address, *args):
    """Handles specific addresses - just prints them normally."""
    print(f"Specific Handler - {address}: {args}")
    # all_messages.append((address, args))

# def update_display():
#     """Formats and prints the latest messages dictionary in place."""
#     latest_messages = {}
#     for address, args in all_messages:
#         latest_messages[address] = args

#     output_string = pprint.pformat(latest_messages)
#     sys.stdout.write("\r\033[K" + output_string)
#     sys.stdout.flush()
last_time = time.time()
def default_handler(address, *args):
    """Handles all other OSC messages."""
    print(address, args)
    global last_time
    message[address] = args
    if len(message) == 7:
        if time.time() - last_time >= 1.0:
            last_time = time.time()
            with open("osc_data.csv", "a") as csvfile:
                # s = ",".join(message.values())
                writer = csv.writer(csvfile)
                row = [i[0] for i in message.values()]
                row.append(datetime.datetime.now().strftime("%H:%M:%S"))
                writer.writerow(row)
            csvfile.close()
           


def save_to_csv(filename="osc_data.csv"):
    """Saves all received OSC messages to a CSV file."""
    headers = [
        '/avatar/parameters/EyesY',
        '/avatar/parameters/LeftEyeLid',
        '/avatar/parameters/LeftEyeLidExpandedSqueeze',
        '/avatar/parameters/LeftEyeX',
        '/avatar/parameters/RightEyeLid',
        '/avatar/parameters/RightEyeLidExpandedSqueeze',
        '/avatar/parameters/RightEyeX'
    ]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write specified header row

        # Create a dictionary to hold the last received value for each parameter
        last_values = {}
        
        for address, values in all_messages:
          if address in headers:
            last_values[address] = values[0] if values else ""

        # Write the last values to the csv file.
        if all(header in last_values for header in headers):
          row = [last_values[header] for header in headers]
          writer.writerow(row)
        else:
          print("Warning: Not all specified addresses were received. CSV may be incomplete.")

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

with open("osc_data.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)  # Write specified header row
csvfile.close()
dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 9000

print(f"Listening for OSC messages on {ip}:{port}...")
print("Press Ctrl+C to exit.")
sys.stdout.write("\033[K")
os.system('cls' if os.name == 'nt' else 'clear')
sys.stdout.flush()

server = BlockingOSCUDPServer((ip, port), dispatcher)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
    # save_to_csv()  # Save data to CSV before exiting
    sys.exit(0)