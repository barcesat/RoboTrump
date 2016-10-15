from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
import cv2



first = True
average = 0


def findFace(callback, state):

	print('starting find face')
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	time.sleep(0.1)

	faceFound = False
	global first
	global average
	turn = "center"

	while state[0] == "greet":

		camera = PiCamera()
		camera.resolution = (640, 480)
		camera.framerate = 32
		rawCapture = PiRGBArray(camera, size=(640, 480))

		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			print('continues coature')
	        	image = frame.array
	
			if state[0] != "greet":
				break
		
		        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		
		        for (x,y,w,h) in faces:
			    print('found face')
		            faceFound = True
		            newx = (x + w/2) - w/16
		            newy = (y + y/2) - y/16
		            colorbox = gray[newy:(newy+(h/8)), newx:(newx+(w/8))]
		#get average color of pixels in colorbox
		            #average_color_per_row = np.average(colorbox,axis=0)
		            #average_color = np.average(average_color_per_row,axis=0)
		            #average_color = np.uint8(average_color)
		            #average_color_image = np.array([[average_color]*100]*100, np.uint8)
		#or alternatively get maxcolor of pixels in colorbox (lightest color) so we can avoid eyebrows/eyes/hair
		            if (len(colorbox) != 0):
		                max_color_per_row = np.max(colorbox,axis=0)
		                max_color = np.max(max_color_per_row,axis=0)
		                max_color = np.uint8(max_color)
		                #max_color_image = np.array([[max_color]*100]*100, np.uint8)
		#make a square in that color in the top left corner of the image
		            #image[0:100, 0:100] = max_color_image
		            #print(max_color)
		
		                if (first == True):
		                    average = max_color
		                    first = False
		                else:
		                    average = (average + max_color)/2
		
		            point = x + (w/2)
		            if (point >= 427):
		                turn = "right"
		            elif (point < 427 and point > 213):
		                turn = "center"
		            else:
		                turn = "left"
		        #cv2.imshow("Frame", image)
		        key = cv2.waitKey(1) & 0xFF
		
		        if key == ord("q"):
		            break
		        if (faceFound):
		            print("camera closed")
		            insult = calculateInsult(max_color, turn)
		            callback(insult, turn)
			    faceFound = False
			    break
		            #return
		
        		rawCapture.truncate(0)
		camera.close()


def calculateInsult(face, turn):
    global average
    insult = 10
    step = 12.75
    text = turn

    if (face >= average):
        insult = 10
        insult += np.floor_divide((face-average), step)
    else:
        insult = 10
        insult -= np.floor_divide((average-face), step)
    
    return insult


#Receive start command from main feed
#findFace()
    
    
    


