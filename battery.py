# chatGPT generated script
from gpiozero import DigitalOutputDevice, PWMOutputDevice, Button
from time import sleep

import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BCM)
Green_LED = 23
Yellow_LED = 24
Red_LED = 25

GPIO.setup(Green_LED, GPIO.OUT)
GPIO.setup(Yellow_LED, GPIO.OUT)
GPIO.setup(Red_LED, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000

class DCMotor:
# initiates pins 1, 2, and pwm as output pins
    def __init__(self, pin1, pin2, enable_pin):
        self.in1 = DigitalOutputDevice(pin1)
        self.in2 = DigitalOutputDevice(pin2)
        self.pwm = PWMOutputDevice(enable_pin)

# these are the parameters for the motor to move forward
    def forward(self, speed):
        self.in1.on()
        self.in2.off()
        self.pwm.value = min(max(speed, 0),1)

# these are the parameters for the motor to move backward
    def backwards(self, speed):
        self.in1.off()
        self.in2.on()
        self.pwm.value = min(max(speed, 0),1)
        
# these are the parameters for the motor to stop, pins 1 & 2 are turned off        
    def stop(self):
        self.pwm.value = 0
        self.in1.off()
        self.in2.off()
        
motor1 = DCMotor(pin1=2, pin2=3, enable_pin=4)
motor2 = DCMotor(pin1=17, pin2=27, enable_pin=22)

# read data from MCP3008, channels 0-7 on the chip
def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) <<8) + adc[2]
    return data

def convert_to_voltage(adc_value):
    return (adc_value * 3.3)/1023

def convert_to_battery_voltage(measured_voltage):
    return measured_voltage * ((10 + 3.3)/3.3)

# initialize the LEDs to be turned off
def show_leds(battery_voltage):
    GPIO.output(Green_LED, False)
    GPIO.output(Yellow_LED, False)
    GPIO.output(Red_LED, False)
    
    # range of battery levels
    if battery_voltage > 10:
        GPIO.output(Green_LED, True)
    elif 5 <= battery_voltage <= 7.5:
        GPIO.output(Yellow_LED, True)
    else:
        GPIO.output(Red_LED, True)
        
motor1.forward(0)
motor2.forward(0)
        
try:
    while True:
        adc_value = read_adc(0)
        measured_voltage = convert_to_voltage(adc_value)
        battery_voltage = convert_to_battery_voltage(measured_voltage*2.4)
        print(f"battery voltage: {battery_voltage:.2f} V")
        
        show_leds(battery_voltage)
        time.sleep(1)
        
except KeyboardInterrupt:
    print("exiting")
    GPIO.cleanup()
    spi.close()

