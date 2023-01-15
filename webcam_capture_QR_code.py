#!./venv/bin/python3
#######
#
# This script is a QR-code scanner. It turns on your webcam, waits for you to show it a QR-code, decodes it, extracts the data, prints it out, and exits. If your QR-code is a COVID vaccination certificate, the output will be a base45 string that you can recognize by the "HC1:" prefix.
#
#######

from contextlib import contextmanager
import cv2
from pyzbar import pyzbar
import sys

@contextmanager
def managed_videocapture():
    # Code to acquire resource, e.g.:
    cap = cv2.VideoCapture(0)
    try:
        yield cap
    finally:
        # Code to release resource, e.g.:
        cap.release()


if __name__ == "__main__":
    # Initialize webcam stream
    with managed_videocapture() as cap:
        # Check if the webcam is opened correctly
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
            sys.exit()
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Display the resulting frame
            frame = cv2.resize(frame, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)
            cv2.imshow("Press any key to interrupt capturing video...", frame)
            # if cv2.waitKey(1) & 0xFF == ord(exit_key):
            if cv2.waitKey(1) != -1:
                break
            # Find QR codes in the frame
            decoded_objs = pyzbar.decode(frame)
            # If QR code is found
            if decoded_objs:
                for obj in decoded_objs:
                    if isinstance(obj.data, str):
                        print(obj.data)
                    elif isinstance(obj.data, bytes):
                        print(obj.data.decode())
                break
