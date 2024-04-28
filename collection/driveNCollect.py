from robot_hat.utils import reset_mcu
from picarx import Picarx
from picamera2 import Picamera2, Preview
from time import sleep, strftime, localtime
import readchar
import os
from vilib import Vilib

px = Picarx()
path = "/home/rohan/dl/picar-x/collection/track1"
#user_home = os.path.expanduser(f'~{user}')

def take_photo(angle, speed, status):
    try:
        folder_name = "track1" 
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        fileName = f"{folder_name}_time_{strftime('%Y%m%d_%H%M%S', localtime())}_angle_{angle}_speed_{speed}_status_{status}"
    
        #Capture image
        Vilib.take_photo(fileName, path)
        print('\nphoto save as %s%s'%(path,fileName))
    except Exception as e:
        print(f"Error occurred while saving image: {e}")

def move(operate:str, speed):
    if operate == 'stop':
        px.stop()
        take_photo(0, speed, "stop")
    else: 
        if operate == 'forward':
            px.set_dir_servo_angle(0)
            px.forward(speed)
            take_photo(0, speed, "forward")
        elif operate == 'backward':
            px.set_dir_servo_angle(0)
            px.backward(speed)
            take_photo(0, speed, "backward")
        elif operate == 'turn left':
            px.set_dir_servo_angle(-30)
            px.forward(speed)
            take_photo(-30, speed, "turn left")
        elif operate == 'turn right':
            px.set_dir_servo_angle(30)
            px.forward(speed)
            take_photo(30, speed, "turn right")


def main():
    try:
        Vilib.camera_start(vflip=False,hflip=False)
        Vilib.display(local=True,web=True)
        sleep(2)
        speed = 0
        status = 'stop'

        while True:
            print("\rstatus: %s , speed: %s    "%(status, speed), end='', flush=True)
            # readkey
            key = readchar.readkey().lower()
            # operation 
            if key in ('wsadfop'):
                # throttle
                if key == 'o':
                    if speed <=90:
                        speed += 10           
                elif key == 'p':
                    if speed >=10:
                        speed -= 10
                    if speed == 0:
                        status = 'stop'
                # direction
                elif key in ('wsad'):
                    if speed == 0:
                        speed = 1
                    if key == 'w':
                        # Speed limit when reversing,avoid instantaneous current too large
                        if status != 'forward' and speed > 60:  
                            speed = 60
                        status = 'forward'
                    elif key == 'a':
                        status = 'turn left'
                    elif key == 's':
                        if status != 'backward' and speed > 60: # Speed limit when reversing
                            speed = 60
                        status = 'backward'
                    elif key == 'd':
                        status = 'turn right' 
                # stop
                elif key == 'f':
                    status = 'stop'
                # move 
                move(status, speed)  
            # take photo
            elif key == 't':
                take_photo()
            # quit
            elif key == readchar.key.CTRL_C:
                print('\nquit ...')
                px.stop()
                break 

            sleep(0.1)
    except Exception as e:
        print("error:%s"%e)
    finally:
        Vilib.camera_close()
        px.stop()

if __name__ == "__main__":
    main()
