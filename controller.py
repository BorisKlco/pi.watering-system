import RPi.GPIO as GPIO

# GPIO/BCM Number
GPIO.setmode(GPIO.BCM)

# Physical/Board pin
# GPIO.setmode(GPIO.BOARD)


class Relay:
    def __init__(self, pin):
        self.pin = pin

    def init(self, name):
        GPIO.setup(self.pin, GPIO.OUT)
        print(name, "- GPIO.OUT init...")

    def on(self):
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH)


class Sensor:
    def __init__(self, pin):
        self.pin = pin

    def init(self, name):
        GPIO.setup(self.pin, GPIO.IN)
        print(name, "GPIO.IN init...")

    def output(self):
        return GPIO.input(self.pin)
