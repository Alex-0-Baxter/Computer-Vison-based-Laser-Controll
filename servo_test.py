from gpiozero import Servo
from time import sleep

# Define the servo pin (replace '17' with your GPIO pin number)
servo = Servo(18)

def test_servo_range():
    try:
        print("Testing servo range...")

        # Start at the neutral position
        print("Moving to neutral (0)...")
        servo.value = 0
        sleep(1)

        # Gradually move to the minimum position (-1)
        print("Testing minimum range...")
        for value in [-0.8, -0.9, -1.0]:
            servo.value = value
            print(f"Position: {value}")
            sleep(0.5)

        # Gradually move to the maximum position (+1)
        print("Testing maximum range...")
        for value in [0.8, 0.9, 1.0]:
            servo.value = value
            print(f"Position: {value}")
            sleep(0.5)

        print("Servo range test complete!")
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Return the servo to the neutral position when done
        print("Returning to neutral position.")
        servo.value = 0
        sleep(1)

if __name__ == "__main__":
    test_servo_range()
