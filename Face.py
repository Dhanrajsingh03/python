import cv2
from deepface import DeepFace

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set frame resolution (optional, improves performance)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Loading DeepFace model... (this may take some time)")
try:
    # Load DeepFace model outside the loop for better performance
    DeepFace.analyze(img_path="test.jpg", actions=['emotion'], enforce_detection=False)
    print("Model loaded successfully!")
except Exception as e:
    print("DeepFace initialization failed:", e)
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    try:
        # Analyze the emotion in the frame
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        if isinstance(result, list) and len(result) > 0 and 'dominant_emotion' in result[0]:
            dominant_emotion = result[0]['dominant_emotion']
        else:
            dominant_emotion = "Unknown"

        # Display the detected emotion on the frame
        cv2.putText(frame, f"Emotion: {dominant_emotion}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    except Exception as e:
        print("Error in detecting emotion:", e)
        cv2.putText(frame, "Error detecting emotion", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Show the frame
    cv2.imshow("Facial Expression Detection", frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
