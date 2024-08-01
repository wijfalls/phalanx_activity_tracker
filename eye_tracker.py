import cv2
import dlib

def track_eye_position():
    # Load the pre-trained face detector and shape predictor from dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = detector(gray)
        for face in faces:
            # Get the landmarks/parts for the face in box d.
            shape = predictor(gray, face)

            # Draw circles around the eyes
            for i in range(36, 42):  # Right eye
                x = shape.part(i).x
                y = shape.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for i in range(42, 48):  # Left eye
                x = shape.part(i).x
                y = shape.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # Display the frame with eye tracking
        cv2.imshow('Eye Tracking', frame)

        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_eye_position()
