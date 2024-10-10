import zmq
import cv2
import pyrealsense2 as rs
import base64
from math import atan2

context = zmq.Context()

control_socket = context.socket(zmq.REP)
control_socket.bind("tcp://*:5555")

camera_socket = context.socket(zmq.PUSH)
camera_socket.connect("tcp://localhost:5556")


droidcam_url = "http://192.168.110.27:4747/video"

# camera = cv2.VideoCapture(droidcam_url)
# camera = cv2.VideoCapture(3)
pipeline = rs.pipeline()
config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.rgb8, 30)
profile = pipeline.start(config)

device = profile.get_device()

color_sensor = profile.get_device().query_sensors()[1]
color_sensor.set_option(rs.option.auto_exposure_priority, True)

print("Server is running...")

while True:
    try:
        message = control_socket.recv_json()

        theta = atan2(dy, dx)

        dx = message['dx']
        dy = message['dy']
        velocity = message['velocity']

        print(f"Received direction: ({dx}, {dy}), velocity: {velocity}")
    
        response = f"Direction ({dx}, {dy}), velocity {velocity} received"
        control_socket.send_string(response)

        # ret, frame = camera.read()

        if not ret:
            print("Failed to capture frame")
            break
        else:
            print("Frame captured")
        # frame = cv2.resize(frame, (640, 480))

        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = buffer.b64encode(encoded)
        camera_socket.send(jpg_as_text)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        # camera.release()
        cv2.destroyAllWindows()
