import cv2
import numpy as np
from pyzbar.pyzbar import decode


def decode_qr_code(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode QR codes
    decoded_objects = decode(gray)

    # Loop over all detected QR codes
    for obj in decoded_objects:
        # Extract the data and bounding box of the QR code
        data = obj.data.decode("utf-8")
        rect_points = obj.polygon

        # Draw a rectangle around the QR code
        if len(rect_points) > 4:
            hull = cv2.convexHull(np.array([point for point in rect_points], dtype=np.float32))
            cv2.drawContours(frame, [hull], -1, (255, 0, 0), 3)
        else:
            cv2.polylines(frame, [np.array(rect_points, dtype=np.int32)], True, (255, 0, 0), 2)

        # Put the decoded data on the frame
        cv2.putText(frame, data, (rect_points[0][0], rect_points[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Print the decoded data to the console
        print("Decoded Data:", data)


# Open the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Decode QR codes in the frame
    decode_qr_code(frame)

    # Display the frame
    cv2.imshow('QR Code Scanner', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
