import board
import displayio
import adafruit_display_shapes.rect as rect
import adafruit_display_text.label as label
import adafruit_matrixportal.matrix as matrix
from adafruit_matrixportal.network import Network
import time

# Initialize the Matrix display
matrix_display = matrix.Matrix(width=64, height=32)
display = matrix_display.display

# Define the network
network = Network(
    status_neopixel=board.NEOPIXEL,
    debug=True
)
network.connect()

# Use the network instance to make requests
requests = network.requests

# Fetch data from CitiBike API
STATION_STATUS_DATA = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
STATION_INFO_DATA = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"

station_id = "457"

def load_data(url):
    response = requests.get(url)
    data = response.json()
    stations = data["data"]["stations"]
    for station in stations:
        if station["station_id"] == station_id:
            return station

station_status = load_data(STATION_STATUS_DATA)
station_info = load_data(STATION_INFO_DATA)

def format_time(timestamp):
    t = time.localtime(timestamp)
    return time.strftime("%I:%M %p", t)

def display_data(status, info):
    display.fill(0)  # Clear the display

    # Create a group for display
    group = displayio.Group()

    # Display station name
    station_label = label.Label(
        text=info["name"], color=0xFFFFFF, x=0, y=0
    )
    group.append(station_label)

    # Display last reported time
    last_reported_time = format_time(status["last_reported"])
    time_label = label.Label(
        text=last_reported_time, color=0xFFFFFF, x=0, y=10
    )
    group.append(time_label)

    # Display number of bikes
    bikes = status["num_bikes_available"]
    bikes_label = label.Label(
        text=f"Bikes: {bikes}", color=0xFFFFFF, x=0, y=20
    )
    group.append(bikes_label)

    # Display number of e-bikes
    ebikes = status["num_ebikes_available"]
    ebikes_label = label.Label(
        text=f"E-Bikes: {ebikes}", color=0xFFFFFF, x=0, y=30
    )
    group.append(ebikes_label)

    # Add group to the display
    display.show(group)

# Show data on the display
display_data(station_status, station_info)

while True:
    time.sleep(60)  # Refresh every 60 seconds
