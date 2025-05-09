import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from gpiozero import Servo
import time

# Set up the camera with Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 1280)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the YOLOv8 model
#Make sure model is set fro ARM Framework using modle conversion.py file
model = YOLO("yolov8s-world.pt")

# Define custom classes to track
custom_classes = ["black book", "white book"]
model.set_classes(custom_classes)

# Set up servos for pan and tilt control
pan_servo = Servo(17)  # GPIO pin 17 for pan servo
tilt_servo = Servo(18)  # GPIO pin 18 for tilt servo
pan_servo.value = 0  # Center pan servo
tilt_servo.value = 0  # Center tilt servo
time.sleep(1)  # Allow servos to initialize

# Helper function to map values
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Variables to store the current servo positions
current_pan_position = 0
current_tilt_position = 0

# Servo step for smooth movement
servo_step = 0.02  

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()
    
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Run YOLO model on the captured frame
    results = model(frame, imgsz=160)

    # Annotate the frame with detection results
    annotated_frame = results[0].plot()

    # Get bounding boxes and object classes
    boxes = results[0].boxes  # Bounding box data
    if len(boxes) > 0:  # Check if objects are detected
        for box in boxes:
            obj_class = int(box.cls)  # Class ID of the detected object
            class_name = custom_classes[obj_class] if obj_class < len(custom_classes) else "unknown"
            
            if class_name in custom_classes:  # Process only custom objects
                x1, y1, x2, y2 = box.xyxy[0]  # Coordinates of the bounding box
                confidence = box.conf[0]  # Confidence
                
                # Calculate the center of the detected object
                obj_center_x = (x1 + x2) / 2
                obj_center_y = (y1 + y2) / 2
                frame_width = frame.shape[1]
                frame_height = frame.shape[0]

                # Map the object's position to servo range (-1 to 1)
                target_pan_position = map_value(obj_center_x, 0, frame_width, -1, 1)
                target_tilt_position = map_value(obj_center_y, 0, frame_height, 1, -1)  # Invert Y direction for servo

                # Smoothly move the pan servo to the target position
                if abs(target_pan_position - current_pan_position) > servo_step:
                    current_pan_position += servo_step * (1 if target_pan_position > current_pan_position else -1)
                else:
                    current_pan_position = target_pan_position

                # Smoothly move the tilt servo to the target position
                if abs(target_tilt_position - current_tilt_position) > servo_step:
                    current_tilt_position += servo_step * (1 if target_tilt_position > current_tilt_position else -1)
                else:
                    current_tilt_position = target_tilt_position

                pan_servo.value = current_pan_position
                tilt_servo.value = current_tilt_position

                
                print(f"Detected {class_name} - Confidence: {confidence:.2f}, Center (X, Y): ({obj_center_x:.2f}, {obj_center_y:.2f}), Pan Pos: {current_pan_position:.2f}, Tilt Pos: {current_tilt_position:.2f}")

    else:
        # No objects detected, reset servos to center
        if abs(0 - current_pan_position) > servo_step:
            current_pan_position += servo_step * (-1 if current_pan_position > 0 else 1)
        else:
            current_pan_position = 0
        if abs(0 - current_tilt_position) > servo_step:
            current_tilt_position += servo_step * (-1 if current_tilt_position > 0 else 1)
        else:
            current_tilt_position = 0

        pan_servo.value = current_pan_position
        tilt_servo.value = current_tilt_position

    # Display the annotated frame
    cv2.imshow("Camera", annotated_frame)

    
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
