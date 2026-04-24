from multiprocessing import Process

#def start_motor():
    #import motor_code
    #motor_code.run()
    
def start_camera():
    import camera
    camera.run()

def start_battery():
    import battery
    battery.run()
    
if __name__ == "main":
    processes = [
        #Process(target = start_motor),
        Process(target = start_camera),
        Process(target = start_battery),
    ]
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
