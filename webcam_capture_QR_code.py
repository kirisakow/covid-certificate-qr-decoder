#!./venv/bin/python3
#######
#
# This script is a QR-code scanner. It turns on your webcam, waits for you to show it a QR-code, decodes it, extracts the data, prints it out, and exits. If your QR-code is a COVID vaccination certificate, the output will be a base45 string that you can recognize by the "HC1:" prefix.
#
#######

from contextlib import contextmanager
import argparse
import cv2
from pyzbar import pyzbar
import sys

@contextmanager
def managed_videocapture(cam_index):
    # Code to acquire resource, e.g.:
    capture = cv2.VideoCapture(cam_index)
    try:
        yield capture
    finally:
        # Code to release resource, e.g.:
        capture.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Read QR-code with your webcam""",
                                     epilog="Source code: https://github.com/kirisakow/covid-certificate-qr-decoder")
    parser.add_argument('--camera-index', '--camera_index', default=0, type=int, nargs=1,
                    help="(optional, default: %(default)s) Camera index. For desktop machines default is usually 0, for mobile devices it can vary (try 1 or 2).")
    args = parser.parse_args()
    camera_index = args.camera_index[0] if isinstance(args.camera_index, list) else args.camera_index
    # Initialize webcam stream
    with managed_videocapture(camera_index) as cap:
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
