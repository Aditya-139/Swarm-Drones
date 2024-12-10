from djitellopy import Tello
import cv2
import navigation
import data_collection
import model_training
import human_tracking
import obstacle_avoidance
import gun_detection
import stun_device
import counter_drone
import battery_management
from utils import load_model, logger

drone = Tello()
drone.connect()
drone.streamon()
frame_read = drone.get_frame_read()

num_classes = 2  # Adjust based on your dataset
model = load_model("human_model.pth", num_classes)

try:
    navigation.navigate()

    while True:
        frame = frame_read.frame
        frame, human_detected = human_tracking.detect_human(frame)
        frame, gun_detected = gun_detection.detect_gun(frame)
        if gun_detected:
            drone.move_forward(100)
            stun_device.activate_stun_device()
        if human_detected:
            frame = obstacle_avoidance.avoid_obstacles(drone, frame)
        counter_drone.detect_and_neutralize_threats(frame)
        battery_management.monitor_battery(drone)
        cv2.imshow("Drone Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    drone.streamoff()
    cv2.destroyAllWindows()
