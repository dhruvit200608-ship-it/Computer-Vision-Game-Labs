import cv2
from cvzone.HandTrackingModule import HandDetector as Hd
import time

# --- Setup Camera ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width to 1280
cap.set(4, 720)   # Set height to 720

# --- Initialize Variables ---
initialtime = 0
fastest = 1000
finaltime = 10000
t_st = False        # Boolean to track if the timer is currently running
x = "Stop"          # String to display timer status

# --- Initialize Hand Detector ---
# detectionCon: Minimum confidence value for detection
# maxHands: Maximum number of hands to detect
d = Hd(detectionCon=0.5, maxHands=1)

while True:
    # 1. Capture frame and flip it for a mirror effect
    _, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Detect hands in the frame
    # flipType=False because we already flipped the image manually
    hands, img = d.findHands(img, flipType=False)

    if hands:
        for hand in hands:
            # Check if the detected hand is the Left hand
            if hand['type'] == "Left":
                
                # --- START TIMER LOGIC ---
                # Checks for specific finger patterns (e.g., open hand or specific fingers up)
                # fingersUp returns a list [thumb, index, middle, ring, pinky] (1 for up, 0 for down)
                if d.fingersUp(hands[0]) == [0, 1, 1, 1, 1] or d.fingersUp(hands[0]) == [[0, 0, 1, 1, 1]]:
                    if t_st == False:
                        initialtime = time.time()  # Record the start timestamp
                        x = "Start"
                        t_st = True

                # --- STOP TIMER LOGIC ---
                # Checks if all fingers are down (fist)
                if d.fingersUp(hands[0]) == [0, 0, 0, 0, 0]:
                    if t_st:
                        # Calculate elapsed time and round to 2 decimal places
                        finaltime = (int((time.time() - initialtime) * 100)) / 100
                        print(finaltime)
                        
                        # Update the "Fastest" record if the current time is lower
                        if fastest > finaltime:
                            fastest = finaltime
                            print(f"New fastest {fastest}")
                            # Visual feedback for a new record
                            cv2.putText(img, str(f"New fastest is {fastest}").zfill(2), (50, 100), 
                                        cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 3)
                        
                        x = "Stop"
                        t_st = False

    # 3. Update the running timer display if the timer is active
    if t_st:
        finaltime = (int((time.time() - initialtime) * 100)) / 100

    # --- UI Overlays ---
    # Display current status (Start/Stop)
    cv2.putText(img, str(f"timer status {x}"), (500, 650), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)
    
    # Display the personal best (fastest) time
    cv2.putText(img, str(f"fastest is {fastest}").zfill(2), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 3)
    
    # Display the current/last recorded time
    cv2.putText(img, str(finaltime), (25, 650), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)

    # 4. Show the result and handle exit
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)