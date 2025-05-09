import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from gpiozero import LED

# Set up the camera with Picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 1280)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Initialize frame counter and average FPS
av_frames = 0
i = 0

# Load our YOLOv8 model
model = YOLO("yolov8s-world.pt")

# Define custom classes
model.set_classes(["black book", "white book"])

# # GPIO LED setup
# red = LED(17)
# blue = LED(27)
# green = LED(22)

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()
    
    # Run YOLO model on the captured frame
    results = model(frame, imgsz=160)
    
    # Annotate the frame with detection results
    annotated_frame = results[0].plot()

    # Get inference time and calculate FPS
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time  # Convert to milliseconds
    av_frames += fps
    i += 1

    # Display FPS on the frame
    text = f'FPS: {fps:.1f}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = annotated_frame.shape[1] - text_size[0] - 10
    text_y = text_size[1] + 10
    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Get bounding boxes and object classes
    boxes = results[0].boxes  # All bounding box data
    for box in boxes:
        # Extract bounding box details
        x1, y1, x2, y2 = box.xyxy[0]  # Coordinates of the box
        obj_class = int(box.cls)     # Class ID of the object
        confidence = box.conf[0]     # Confidence score
        
        # Print object details
        print(f"Detected object - Class: {obj_class}, Confidence: {confidence:.2f}, Position: ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f})")
        
#         # Check if the object matches the specified classes
#         if obj_class in objects_to_detect:
#             if obj_class == 0:  # Example: Person
#                 green.on()
#             elif obj_class == 16:  # Example: Bear
#                 blue.on()
#             elif obj_class == 21:  # Example: Dog
#                 red.on()
#         else:
#             green.off()
#             blue.off()
#             red.off()

    # Display the annotated frame
    cv2.imshow("Camera", annotated_frame)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        num = av_frames / i
        print(f"Average FPS: {num}")
        break

# Close all windows and clean up
cv2.destroyAllWindows()
