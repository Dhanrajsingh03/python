import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import pygetwindow as gw  # To properly minimize the active window

# Initialize Mediapipe hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Start video capture
cap = cv2.VideoCapture(0)

# Get camera frame size
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Store previous position for smooth movement
prev_x, prev_y = 0, 0
smooth_factor = 5  # Controls smoothness of movement

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue
    frame = cv2.flip(frame, 1)  # Mirror the frame
    h, w, _ = frame.shape  # Get frame size dynamically
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger landmarks
            index_finger = hand_landmarks.landmark[8]  # Index finger tip
            thumb = hand_landmarks.landmark[4]  # Thumb tip
            middle_finger = hand_landmarks.landmark[12]  # Middle finger tip
            little_finger = hand_landmarks.landmark[20]  # Little finger tip
            
            # Convert hand coordinates to screen space
            x = int(index_finger.x * w)
            y = int(index_finger.y * h)

            # 🛠 **Fix Scaling Issue: Properly Map to Full Screen**
            screen_x = int(np.interp(x, [50, w - 50], [0, screen_width]))  
            screen_y = int(np.interp(y, [50, h - 50], [0, screen_height]))  

            # 🌀 **Smooth Movement**
            smooth_x = prev_x + (screen_x - prev_x) / smooth_factor
            smooth_y = prev_y + (screen_y - prev_y) / smooth_factor
            pyautogui.moveTo(smooth_x, smooth_y)
            prev_x, prev_y = smooth_x, smooth_y

            # Measure distances for gestures
            thumb_index_dist = np.hypot(index_finger.x - thumb.x, index_finger.y - thumb.y)
            thumb_middle_dist = np.hypot(middle_finger.x - thumb.x, middle_finger.y - thumb.y)
            thumb_little_dist = np.hypot(little_finger.x - thumb.x, little_finger.y - thumb.y)

            # **Left Click (Thumb & Index Finger Pinch)**
            if thumb_index_dist < 0.05:
                pyautogui.click()
                cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # **Right Click (Thumb & Middle Finger Pinch)**
            if thumb_middle_dist < 0.05:
                pyautogui.rightClick()
                cv2.putText(frame, "Right Click", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # **Minimize Window (Thumb & Little Finger Touch)**
            if thumb_little_dist < 0.05:
                active_window = gw.getActiveWindow()
                if active_window:
                    active_window.minimize()  # Minimize the active window
                    cv2.putText(frame, "Minimized", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # **Scroll Up & Down (Move Hand Up/Down)**
            if y < h // 3:  # Upper part of the screen
                pyautogui.scroll(10)  # Scroll up
                cv2.putText(frame, "Scroll Up", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            elif y > 2 * (h // 3):  # Lower part of the screen
                pyautogui.scroll(-10)  # Scroll down
                cv2.putText(frame, "Scroll Down", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Gesture Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
