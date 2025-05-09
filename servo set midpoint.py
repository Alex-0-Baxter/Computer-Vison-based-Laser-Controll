from gpiozero import Servo
from time import sleep

# Create a Servo object attached to a specific GPIO pin (e.g., GPIO17)
servo = Servo(18)

# Set the servo to its middle position
servo.value = 0  # 0 corresponds to the middle position of the servo

# Optionally, wait for a while to observe the position
sleep(2)
