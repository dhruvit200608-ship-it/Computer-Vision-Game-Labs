# Computer Vision Labs

This repository contains a suite of interactive applications exploring **Human-Computer Interaction (HCI)** through real-time Computer Vision. By leveraging hand-tracking landmarks, these projects translate physical movement into digital commands.

## Featured Projects

### 1. Vision-Pong
A classic arcade experience where the paddle is controlled by the user's hand position.
- **Technology:** OpenCV, Cvzone (HandTrackingModule).
- **Logic:** Maps the Y-coordinate of the hand landmark to the paddle position, implementing collision physics and score tracking.

### 2. Touchless Cube Timer
A productivity tool for speedcubers that allows the user to start and stop a timer without touching the keyboard.
- **Technology:** MediaPipe, Python Time module.
- **Logic:** Uses gesture recognition (finger-up/finger-down states) to trigger timer states, preventing physical contact with the device.

## Technical Stack
- **Language:** Python 3.x
- **Libraries:** - `opencv-python` (Real-time video processing)
  - `cvzone` (Hand landmark abstraction)
  - `numpy` (Coordinate math)
