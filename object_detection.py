import cv2
import torch
from utils import load_model, transform_image, handle_errors

# Load YOLOv5 model
model_path = "model.pth"
num_classes = 10  # Adjust based on your dataset
model = load_model(model_path, num_classes)

@handle_errors
def detect_objects(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_tensor = transform_image(frame_rgb)
    
    outputs = model(input_tensor)
    _, predicted = torch.max(outputs, 1)
    class_id = predicted.item()
    
    cv2.putText(frame, f"Class: {class_id}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return frame
