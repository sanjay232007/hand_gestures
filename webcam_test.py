
import cv2

# Open the default webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    raise SystemExit(1)

print("Webcam started. Press 'q' to quit.")

while True:
    # Read one frame from the webcam
    success, frame = cap.read()

    if not success:
        print("Error: Could not read webcam frame.")
        break

    # Mirror the image like a front-facing mirror
    frame = cv2.flip(frame, 1)

    # Display the webcam frame
    cv2.imshow("Hand Gesture Cursor - Webcam Test", frame)

    # Exit when q is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
