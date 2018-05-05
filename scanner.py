import RPi.GPIO as gpio
import picamera
import time

#camera = picamera.PiCamera()
#camera.capture('/home/pi/image.jpg')

#camera.start_preview()
#camera.vflip = True
#camera.hflip = True
#camera.brightness = 60

#camera.start_recording('video.h264')
#time.sleep(5)
#camera.stop_recording()

scan = 0
etat = 1
delai = 2

gpio.setmode(gpio.BCM)

# stepper motor pins
gpio.setup(23,gpio.OUT) # in1 - L298N
gpio.setup(24,gpio.OUT) # in2 - L298N
gpio.setup(25,gpio.OUT) # in3 - L298N
gpio.setup(26,gpio.OUT) # in4 - L298N
StepPins = [23,24,25,26]

# control board
gpio.setup(5,gpio.OUT) # green
gpio.setup(6,gpio.OUT) # red
gpio.setup(19,gpio.IN, pull_up_down=gpio.PUD_DOWN) # stop
gpio.setup(20,gpio.IN, pull_up_down=gpio.PUD_DOWN) # +
gpio.setup(21,gpio.IN, pull_up_down=gpio.PUD_DOWN) # -

# L298N initialization
gpio.output(23, False)
gpio.output(24, False)
gpio.output(25, False)
gpio.output(26, False)

stepAngle = 7.5
nbStep = 360/stepAngle
StepCounter = 0
WaitTime = 0.5

StepCount1 = 4
Seq1 = [[1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]]

# Initializing output pin sequence
StepCount2 = 8
Seq2 = [[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]


gpio.add_event_detect(19, gpio.RISING)
def my_scan_stop_and_go(self):
#    print ("stop")
    global scan
    if scan == 0 :
        scan = 1
    else :
        scan = 0
gpio.add_event_callback(19, my_scan_stop_and_go)

gpio.add_event_detect(21, gpio.RISING)
def my_stop(self):
#    print ("stop")
    global etat
    if etat == 0 :
        etat = 1
    else :
        etat = 0
gpio.add_event_callback(21, my_stop)

def my_turn():
    global StepCounter
    global StepPins
    
    for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
#            print " Step %i Enable %i" %(StepCounter,xpin)
            gpio.output(xpin, True)
        else:
            gpio.output(xpin, False)
            StepCounter += 1



#camera.vflip = True
#camera.hflip = True
#camera.brightness = 60

#camera.start_recording('video.h264')
#sleep(5)
#camera.stop_recording()
photo = 0

Seq = Seq1
StepCount = StepCount1


while etat==1:
    while (etat==1) and (scan==0):
        gpio.output(5,gpio.HIGH);
        gpio.output(6,gpio.LOW);

    while (etat==1) and (scan==1) and (photo<=360):
        gpio.output(5,gpio.LOW);
        gpio.output(6,gpio.HIGH);
        #take picture and store
        print ("Tourner le plateau")
        my_turn()
        if (StepCounter==StepCount):
            StepCounter = 0
        if (StepCounter<0):
            StepCounter = StepCount
        time.sleep(.5)
        print ("Prise de la photo #",photo+1)
        photo += 1
    if photo>360 :
        print ("Fin du scan")
        etat=0
    else :
        print ("Scan annulé")
    photo = 0
    scan = 0

gpio.output(5,gpio.LOW);
gpio.output(6,gpio.LOW);

#print (delai)



