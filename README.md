# RoboTrump
A robotic incarnation of Donald Trump

https://www.youtube.com/watch?v=opKqUviw3y8

In the news:
http://www.telecomnews.co.il/GeekCon-2016-של-המייקרים-הישראלים-הסתיים-עם-פרויקטים-מרשימים-במיוחד.html

Videos:
https://www.youtube.com/watch?v=PjFj2N0UA4U

Photos:


## How to Build Him

### SETTING UP THE RASPBERRY PI

1) download and prep the pi with raspbian
https://www.raspberrypi.org/downloads/raspbian/

2) run the pi and do raspi-config for:
 enable ssh
 disable uart
 force audiooutput  through 3.5mm 
 enable VNC server
 expand filesystem
 Internationalisation - change to en_US
 enable camera

3) update python and install libraries:

camera:
sudo apt-get install python-opencv

4) download the code from github

5) setup local hotspot using this guide
https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point?view=all
test with a mobile phone: connect to the Access Point

### SETTING UP ROBOT BODY/MOTORS

1) connect the arduino to the servos according to this schematic
[schematic]

2) program it using the provided sketch

3) test servos with processing application https://github.com/barcesat/KinectRobotArm/tree/master/Processing/Servo_control

4) connect the motors, wheels, motor driver and battery to the pi like so
[schematic]

5) test the wheels and motors with arduino L298 test program

6) Assemble robot frame from spare parts (or kit)

7) Attach everything together

8) download the app and test it
[app link]

### Enjoy!



