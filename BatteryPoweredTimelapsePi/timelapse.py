#Script to take pic every 'sleepytimer' second. Button on pin 'offpin' will initiate shutdown-sequence.


#importing modules
import picamera
import time
import os
import RPi.GPIO as GPIO

#setting variables for shutdown-pin and how long to pause between capture 
offpin = 3
##(@24fps w 2.5sec pause~24pics/min which makes 1sec timelapse~1min real time):
sleepytimer = 2.5

#setup GPIO: specify that pins are referred to as shown on RPi-Board, set pin 'offpin' to INPUT-mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(offpin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#function for shutting down RPi
def Int_shutdown(channel):
    time.sleep(sleepytimer)
    os.system("shutdown -h now")

#'listen' to 'offpin', ignore new inputs for 2 seconds(2000 milliseconds) after detecting human activity on 'offpin'
GPIO.add_event_detect(offpin, GPIO.FALLING, callback = Int_shutdown, bouncetime = 2000)

#timelapse engine - save pic every 'sleepytimer' seconds to /mnt/stills/img-{timestamp}.jpg
with picamera.PiCamera() as camera:
    for filename in camera.capture_continuous('/mnt/stills/img-{timestamp}.jpg'):
        time.sleep(sleepytimer)

