# cv_control/hand_gesture_control.py

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Load hand gesture detection model (if using one like Mediapipe, load it here)
# For now, let's use basic color thresholding to detect gestures in a certain region

def get_direction_from_gesture(frame):
    # Convert frame to HSV to detect hand in a specific color range
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color range for skin detection (can be adjusted)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Find contours (if using basic gesture detection)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cnt = max(contours, key=lambda x: cv2.contourArea(x))
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2  # Get the center of the bounding box

        # Example: Use the bounding box's center position to determine the direction
        if cx < frame.shape[1] // 3:
            return 0  # Move left
        elif cx > 2 * frame.shape[1] // 3:
            return 1  # Move right
        elif cy < frame.shape[0] // 3:
            return 2  # Move up
        else:
            return 3  # Move down
    return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get direction from gesture
    direction = get_direction_from_gesture(frame)

    # Use the detected direction to control the snake (pass direction to the snake game)

    cv2.imshow('Gesture Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()