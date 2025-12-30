import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector as Hd
import numpy as np
import pyttsx3 as ptx
import mediapipe as mp

ts = ptx.init()
voices = ts.getProperty("voices")
ts.setProperty("voice", voices[1].id)

instructions1= str("1.) Type Single player in mode if you want it single player mode.")
instructions2= str(" 2.) Type Multi player in mode if wanted Multi player mode. ")
print("Press S to exit the game.")
print("Press P to pause the game.")
print("Press C to continue the game.")
print(instructions1)
print(instructions2)
mode= str(input("mode :- "))
if mode== "Multi player":
  Mh= int(input("number of players :- "))
  d = Hd(detectionCon=0.1, maxHands=Mh)
  name1 = str(input("name of team 1 :- "))
  name2 = str(input("name of team 2 :- "))
  till_score = int(input("How many points mach do you want to play :-  "))
elif mode== "Single player":
    name = str(input("name of player :- "))
else :
    print("irrelavent mode")
    quit()

sp= int(input("Enter speed of ball :- "))

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgBackground = cv2.imread("Resources/bag.jpg")
imgGameOver1 = cv2.imread("Resources/fbaggo2.jpg")
imgGameOver2 = cv2.imread("Resources/fbaggo1.jpg")
imgGameOver = cv2.imread("Resources/go.jpg")
imgBall = cv2.imread("Resources/rball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2r.png", cv2.IMREAD_UNCHANGED)

ds = Hd(detectionCon=0.1, maxHands=1)

ballPos = [100,100]
gameover1 = False
gameover2 = False
speedX = sp
speedY = sp
score1 = 0
score2 = 0
go1 = False
go2 = False
gameOver = False
game=False
gamepause=2
score = 0
scorets1=0
scorets2=0
highscore=0
spx=sp
spy=sp

ts.say("Game is starting")
ts.runAndWait()

while True:

  if mode== "Single player":
      _, img = cap.read()
      img = cv2.flip(img, 1)
      imgRaw = img.copy()

      hands, img = ds.findHands(img, flipType=False)

      img = cv2.addWeighted(img, 0.3, imgBackground, 0.7,0)

      if hands:
          for hand in hands:
              x, y, w, h = hand['bbox']
              h1, w1, _ = imgBat1.shape
              y1 = y - h1 // 2
              y1 = np.clip(y1, 20, 415)
              img = cvzone.overlayPNG(img, imgBat1, (59, y1))
              if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1+10:
                      speedX = -speedX
                      spx= -spx
                      ballPos[0] += 30
                      score += 1
              img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
              if 1145 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1+10:
                      speedX = -speedX
                      spx= -spx
                      ballPos[0] -= 30
                      score += 1
      if ballPos[0] < 40 or ballPos[0] > 1200:
          gameOver = True
          ts.say(f"{name} your final score is {score}")
          ts.runAndWait()
          ballPos=[100,100]
          if score>highscore:
              highscore=score


      if gameOver:
          img = imgGameOver
          cv2.putText(img, str(score).zfill(2), (600, 450), cv2.FONT_HERSHEY_COMPLEX, 2.5, (255, 255, 255), 5)
          cv2.putText(img, str(f"Highscore is {highscore}").zfill(2), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 3)


      else:

          if ballPos[1] >= 500 or ballPos[1] <= 10:
              speedY = -speedY
              spy=-spy

          ballPos[0] += speedX
          ballPos[1] += speedY

          img = cvzone.overlayPNG(img, imgBall, ballPos)

          cv2.putText(img, str(name), (50, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
          cv2.putText(img, str(score), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

      img[580:700, 550:763] = cv2.resize(imgRaw, (213, 120))

      cv2.imshow("Image", img)
      key = cv2.waitKey(1)

      if key == ord('p'):
          gamepause=1
      if gamepause==1:
          speedX=0
          speedY=0
          img = imgBackground
          cv2.putText(img, str("Game Paused"), (440, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 5)
          if key == ord('c'):
             gamepause=2
             if gamepause == 2:
              imgBackground = cv2.imread("Resources/bag.jpg")
              cv2.putText(img, str(name), (100, 650), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 5)
              cv2.putText(img, str(score), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
              speedX=spx
              speedY=spy

      if key == ord('r'):
          ballPos = [100, 100]
          speedX = sp
          speedY = sp
          gameOver = False
          score = 0
          spx=sp
          spy=sp
          imgGameOver = cv2.imread("Resources/go.jpg")
          ts.say("Game restarted")
          ts.runAndWait()

  if mode== "Multi player":
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    hands, img = d.findHands(img, flipType=False)

    img = cv2.addWeighted(img, 0, imgBackground, 1, 0)

    key = cv2.waitKey(1)

    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1+10:
                    speedX = -speedX
                    spx=-spx
                    ballPos[0] += 30

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1125 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1+10:
                    speedX = -speedX
                    spx=-spx
                    ballPos[0] -= 30

    if ballPos[0] <= 40:
        speedX = sp
        speedY = sp
        score1 += 1
        scorets2+=1
        if ballPos[0] <= 40:
          ts.say(f"{name2} has {score1} points")
          ts.runAndWait()
        ballPos = [100, 100]

    elif ballPos[0] >= 1200:
        speedX = sp
        speedY = sp
        score2 += 1
        scorets1+=1
        if ballPos[0] >= 1200:
          ts.say(f"{name1} has {score2} points")
          ts.runAndWait()
        ballPos = [100, 100]

    else:

        if ballPos[1] >= 500 or ballPos[1] <= 30:
            speedY = -speedY
            spy=-spy

        ballPos[0] += speedX
        ballPos[1] += speedY

        img = cvzone.overlayPNG(img, imgBall, ballPos)
        cv2.putText(img, str(name1), (25, 650), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)
        cv2.putText(img, str(score2), (450, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 6)
        cv2.putText(img, str(score1), (843, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 6)
        cv2.putText(img, str(name2), (925, 650), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)

    img[580:700, 550:763] = cv2.resize(imgRaw, (213, 120))

    if scorets1 == till_score:
        ts.say(f"{name1} wins the game")
        ts.runAndWait()
        scorets1+=1

    if scorets2 == till_score:
        ts.say(f"{name2} wins the game")
        ts.runAndWait()
        scorets2+=1

    if score1 >= till_score:
        gameover2 = True

        ballPos = [100, 100]

    if score2 >= till_score:
        gameover1 = True
        ballPos = [100, 100]

    if gameover2:
        img = imgGameOver1

    if gameover1:
        img = imgGameOver2

    cv2.imshow("Image", img)

    if key == ord('p'):
        gamepause = 1
    if gamepause == 1:
        speedX = 0
        speedY = 0
        img = imgBackground
        cv2.putText(img, str("Game Paused"), (440, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 5)
        if key == ord('c'):
            gamepause = 2
            if gamepause == 2:
                imgBackground = cv2.imread("Resources/bag.jpg")
                cv2.putText(img, str(name1), (25, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 6)
                cv2.putText(img, str(score2), (450, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 6)
                cv2.putText(img, str(score1), (843, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 6)
                cv2.putText(img, str(name2), (925, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 6)
                speedX = spx
                speedY = spy

    if key == ord('r'):
        ballPos = [100, 100]
        speedX = sp
        speedY = sp
        gameover1 = False
        gameover2 = False
        speaking = True
        score1 = 0
        score2 = 0
        ts.say("Game restarted")
        ts.runAndWait()
        gameOver = False
        mode="Multi player"
        scorets1 = 0
        scorets2 = 0
        score = 0
        spx = sp
        spy = sp

  if key== ord("s"):
      ts.say("thank you for playing")
      ts.runAndWait()
      print("Thank you for playing, goodbye see you next time")
      quit()