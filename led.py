import RPi.GPIO as GPIO
import time

# Define GPIO pin numbers for each LED
GREEN_PIN = 17
ORANGE_PIN = 18
RED_PIN = 27

# Initialize GPIO settings
def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(ORANGE_PIN, GPIO.OUT)
    GPIO.setup(RED_PIN, GPIO.OUT)

# Turn on the GREEN LED
def turn_on_green():
    GPIO.output(GREEN_PIN, GPIO.HIGH)

# Turn on the ORANGE LED
def turn_on_orange():
    GPIO.output(ORANGE_PIN, GPIO.HIGH)

# Turn on the RED LED
def turn_on_red():
    GPIO.output(RED_PIN, GPIO.HIGH)

# Turn off all LEDs
def turn_off_all():
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(ORANGE_PIN, GPIO.LOW)
    GPIO.output(RED_PIN, GPIO.LOW)

# Cleanup GPIO settings on program exit
def cleanup_gpio():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        initialize_gpio()

        # Test the LEDs
        turn_on_green()
        time.sleep(2)  # Keep GREEN LED on for 2 seconds
        turn_off_all()
        time.sleep(1)  # Wait for 1 second

        turn_on_orange()
        time.sleep(2)  # Keep ORANGE LED on for 2 seconds
        turn_off_all()
        time.sleep(1)  # Wait for 1 second

        turn_on_red()
        time.sleep(2)  # Keep RED LED on for 2 seconds
        turn_off_all()

    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()
