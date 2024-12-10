from djitellopy import Tello
import time
import gpsd
from drone_communication import initialize_communication, monitor_swarm
from utils import handle_errors

drone = Tello()
drone.connect()
gpsd.connect()

def get_gps_coords():
    packet = gpsd.get_current()
    return packet.position()

drone.is_leader = True

drones_info = {}
sock = initialize_communication(drones_info)
drone_addresses = [("192.168.10.2", 12345), ("192.168.10.3", 12345)]

@handle_errors
def navigate():
    drone.takeoff()
    while True:
        lat, lon = get_gps_coords()
        drone.position = (lat, lon)
        monitor_swarm(drone, sock, drones_info, drone_addresses)
        time.sleep(1)
    drone.land()
