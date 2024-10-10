import sys
import cv2
import zmq
import base64
import numpy as np


context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.connect('tcp://localhost:5556')

footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')


while True:
    try:
        try:
            frame = footage_socket.recv_string(zmq.NOBLOCK)
            img = base64.b64decode(frame)
            npimg = np.frombuffer(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            cv2.imshow('Receiver', source)
        except zmq.ZMQError:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):                                                                                                                                           break
    except KeyboardInterrupt:
        cv2.destroyAllWindows()