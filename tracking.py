from gpiozero import DigitalOutputDevice, PWMOutputDevice, Button
from time import sleep
import bluetooth
import subprocess
import time

#target_mac = '9C:DA:A8:D6:58:C0'

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

def get_rssi(mac_address):
    cmd = f"hcitool rssi {mac_address}"
    try:
        output = subprocess.check_output(cmd, shell = True).decode(errors='ignore')
        if "RSSI return value" in output:
            raw_rssi = int(output.split()[-1])
            
            #convert to signed 8-bit if needed)
            if raw_rssi > -127:
                raw_rssi -=256
                
            return raw_rssi
    except subprocess.CalledProcessError:
            return None
        
    return None
        
target_mac = '9C:DA:A8:D6:58:C0'
#         result = subprocess.check_output(["hcitool", "rssi", mac_address])
#         rssi = int(result.decode().strip().split()[-1])
#         return rssi
#     except subprocess.CalledProcessError:
#         return None

try:
    
    while True:
        rssi = get_rssi(target_mac)
        if rssi is not None:
            print(f"signal strength: {rssi} dBm")
            motor1.stop()
            motor2.stop()
        else:
            print(f"RSSI: {rssi} dBm")
            
        if rssi > -256:
                print("move forward (device is near)")
                motor1.forward(1)
                motor2.forward(1)
        elif rssi > -250:
                print("slow down")
                motor1.forward(0.5)
                motor2.forward(0.5)
        else:
                print("stop or turn around")
                motor1.stop()
                motor2.stop()
        time.sleep(0.5)

except KeyboardInterrupt:
    motor1.stop()
    motor2.stop()
    print("stopping...")

#     else:
#         print("device not in range")
#     time.sleep(1)


