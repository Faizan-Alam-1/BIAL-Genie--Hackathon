import requests
import os
import FaceAPIConfig as cnfg
import numpy as np
import cv2
import time
import speak
from pyfirmata import Arduino , SERVO , util
from time import sleep

port = 'COM4' # enter you ardunio port.
pin = 8   # Enter your ardunio port.
board = Arduino(port)
board.digital[pin].mode =SERVO


def picture():
    # cap = cv2.VideoCapture("http://192.168.0.103:8080/video")
    cap = cv2.VideoCapture(0)
    while True:
  
        ret, frame = cap.read()
        cv2.imwrite("CapFrame.jpg", frame)
        cv2.imshow("imshow", frame)
        time.sleep(0)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def rotate(pin , angle) :
    board.digital[pin].write(angle)
    sleep(0.015)

def run():
    for i in range(0, 90):
        rotate(pin , i)
    for i in range (90 , 1, -1):
        rotate(pin , i) 


def predict():
    image_path = os.path.join("CapFrame.jpg")
    image_data = open(image_path, "rb")
    subscription_key, face_api_url = cnfg.config()
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    params = {"returnFaceAttributes": "smile"}

    response = requests.post(
        face_api_url, params=params, headers=headers, data=image_data
    )
    response.raise_for_status()
    faces = response.json()

    for face in faces:
        fa = face["faceAttributes"]

    try:
        val = fa["smile"]
        print(int(val * 100))
        v = int(val*100)
        if(v > 80) :
            run()  
        else :
            speak.speak("Smile is not dectected ,  please Smile")            
    except:
        print("Face is not detected")
        speak.speak("Face is not detected , try again")


time.sleep(0)

while 1:

    picture()
    try:
        predict()
    except:
        print("no internet")
        speak.speak("Please connect to Internet")
            
           
        
