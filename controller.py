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
        print(f"{name} - GPIO.OUT - pin {self.pin} - init...")

    def on(self):
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH)


class Sensor:
    def __init__(self, pin):
        self.pin = pin

    def init(self, name):
        GPIO.setup(self.pin, GPIO.IN)
        print(f"{name} - GPIO.IN - pin {self.pin} - init...")

    def output(self):
        return GPIO.input(self.pin)
