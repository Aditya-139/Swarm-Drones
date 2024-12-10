import json
import socket
import threading
import time
from utils import handle_errors

# Configuration for inter-drone communication
PORT = 12345
BUFFER_SIZE = 1024

@handle_errors
def handle_incoming_messages(sock, drones_info):
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = json.loads(data.decode('utf-8'))
        drones_info[addr] = message

@handle_errors
def send_message(sock, message, drone_addresses):
    for addr in drone_addresses:
        sock.sendto(json.dumps(message).encode('utf-8'), addr)

@handle_errors
def initialize_communication(drones_info):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))

    threading.Thread(target=handle_incoming_messages, args=(sock, drones_info)).start()
    
    return sock

@handle_errors
def manage_swarm_formation(drones_info, leader_position):
    for addr, info in drones_info.items():
        if info['role'] == 'follower':
            info['position'] = adjust_position(info['position'], leader_position)

@handle_errors
def adjust_position(follower_position, leader_position):
    return [leader_position[0] + 10, leader_position[1]]

@handle_errors
def monitor_swarm(drone, sock, drones_info, drone_addresses):
    while True:
        message = {
            'role': 'leader' if drone.is_leader else 'follower',
            'position': drone.position,
            'status': 'ok'
        }
        send_message(sock, message, drone_addresses)

        if drone.is_leader:
            manage_swarm_formation(drones_info, drone.position)
        time.sleep(1)
