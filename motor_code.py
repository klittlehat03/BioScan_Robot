# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-dc-motor-micropython/
# chatGPT: implemented the gpiozero module to control the GPIO pins on the raspberry pi
from gpiozero import DigitalOutputDevice, PWMOutputDevice, Button
from time import sleep
# import pyttsx3
import os
import sys
import json
import contextlib
import pyaudio
import io
from vosk import Model, KaldiRecognizer

# engine = pyttsx3.init()
# engine.say("Hello world")
# engine.runAndWait()

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
        
    def go(self):
        print("moving forward")
        motor1.forward()
        motor2.forward()
        
    def stop(self):
        ("stopping...")
        motor1.stop()
        motor2.stop()
        
    def left(self):
        ("turning left")
        motor1.stop()
        motor2.forward()
        
    def right(self):
        ("turning right")
        motor1.forward()
        motor2.stop()

# assinging the motor pins
motor1 = DCMotor(pin1=2, pin2=3, enable_pin=4)
motor2 = DCMotor(pin1=17, pin2=27, enable_pin=22) 
# button = Button(14, pull_up=True, bounce_time =0.1)

model_path = "/home/klittlehat03/vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print(f"Model '{model_path}' was not found. Please check the path.")
    exit(1)
    
sample_rate = 16000
chunk_size = 8192
format = pyaudio.paInt16
channels = 1

model = Model(model_path)
p = pyaudio.PyAudio()
stream = p.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
recognizer = KaldiRecognizer(model, sample_rate)

# configuring the speeds to correspond to a specific LED color


# turn_left = True
# direction = "forward"

os.system('clear')
#print("Listening for command...")

try:
    while True:
        data = stream.read(chunk_size)
        if recognizer.AcceptWaveform(data):
            result_json = json.loads(recognizer.Result())
            text = result_json.get('text', '')
#             if "hey robot" in text:
#                 print("I'm listening...")
#                 if "enter drive mode" in text:
#                     motor1.forward(0.8)
#                     motor2.forward(0.8)
#                 elif "follow me" in text: # needs to have its own declaration and then called into this script
#                     motor1.forward(0.8)
#                     motor2.forward(0.8)
#                 elif "assess patient" in text: # same as above
#                     motor1.forward(0.8)
#                     motor2.forward(0.8)
            if "go" in text:
                print("Moving forward")
                motor1.forward(0.8)
                motor2.forward(0.8)
            elif "stop" in text:
                print("stopping")
                motor1.forward(0.0)
                motor2.forward(0.0)
            elif "left" in text:
                print("turning left")
                motor1.backwards(0.3)
                motor2.forward(0.8)
                sleep(1)
                motor1.forward(0.8)
            elif "right" in text:
                print("tuning right")
                motor1.forward(0.8)
                motor2.backwards(0.3)
                sleep(1)
                motor2.forward(0.8)

except KeyboardInterrupt:
    print("exiting...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    motor1.stop()
    motor2.stop()
# print("Motor 1 running forward...")

# def toggle_turn():
#     global turn_left
#     
#     if turn_left:
#         print("turning left...")
#         motor1.backwards(0)
#         motor2.backwards(1.5)
#     else:
#         print("turning right...")
#         motor1.forward(1.5)
#         motor2.forward(0)
#     
#     turn_left = not turn_left
# def toggle_direction():
#     global direction
#     
#     if direction == "forward":
#         print("switching to backward direction...")
#         motor1.backwards(1.5)
#         motor2.backwards(1.5)
#         direction = "backward"
#     else:
#         print("switching to forward direction...")
#         motor1.forward(0.8)
#         motor2.forward(0.8)
#         direction = "forward"
    
# button.when_pressed = toggle_turn

while True:
    sleep(0.1)


