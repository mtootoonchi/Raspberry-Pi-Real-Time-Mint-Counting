from flask import Flask, Response, render_template
from picamera2 import Picamera2
import cv2
import numpy as np
import time

picam2 = None  # Declare the camera variable

# Code to smooth amount of mints
num_circles_list = []
num_circles_size = 20
num_circles_index = 0
for i in range(num_circles_size):
    num_circles_list.append(0)

def initialize_camera():
    global picam2
    if picam2 is None:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration({"format": "RGB888"}))
        picam2.start()
        # Add camera initialization settings here if needed

def close_camera():
    global picam2
    if picam2 is not None:
        picam2.stop()
        picam2 = None

def generate_frames():
    global num_circles_list
    global num_circles_size
    global num_circles_index
    initialize_camera()  # Ensure camera is initialized before starting the loop

    while True:
        start_time_ns = time.time_ns()

        # Load the image
        frame = picam2.capture_array()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Apply Gaussian blur to reduce noise
        frame_blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(frame_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=50)

        # Check if any circles were detected
        if circles is not None:
            circles = np.round(circles[0, :]).astype(int)
            num_circles_index = num_circles_index % num_circles_size
            num_circles_list[num_circles_index] = len(circles)
            num_circles_index += 1

            # Draw detected circles
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
        else:
            num_circles_index = num_circles_index % num_circles_size
            num_circles_list[num_circles_index] = 0
            num_circles_index += 1

        _, encoded_frame = cv2.imencode('.jpg', frame)  # Encode frame as JPEG

        yield (b'--frame\r\n'
               b'Content-Type: multipart/related; boundary=frame\r\n\r\n' + encoded_frame.tobytes() + b'\r\n')

        # Run video up to 60 FPS
        end_time_ns = time.time_ns()
        elapsed_time_ns = end_time_ns - start_time_ns
        elapsed_time_s = elapsed_time_ns / 1000000000.0
        time.sleep(max((1.0 / 60) - elapsed_time_s, 0))  # Adjust delay based on your needs

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/mints')
    def mints():
        global num_circles
        return str(max(set(num_circles_list), key=num_circles_list.count))

    try:
        app.run(host='0.0.0.0', port=8000, debug=True)
    finally:
        close_camera()  # Close the camera when the program exits
