from djitellopy import Tello
import cv2
import os
import time
from utils import handle_errors

# Initialize the drone
drone = Tello()
drone.connect()
drone.streamon()

# Create a directory for saving data
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

@handle_errors
def collect_data():
    frame_read = drone.get_frame_read()
    while True:
        frame = frame_read.frame
        cv2.imshow("Drone Camera", frame)
        
        # Save frame to disk
        frame_path = os.path.join(data_dir, f"frame_{int(time.time())}.jpg")
        cv2.imwrite(frame_path, frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

try:
    collect_data()
finally:
    drone.streamoff()
    cv2.destroyAllWindows()
