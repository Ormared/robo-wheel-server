import zmq
import signal
import sys
import logging
from typing import NoReturn
from math import atan2

from controller import Controller
from constants import ZMQ_BIND_ADDRESS


def signal_handler(sig, frame):
    print('Shutting down server...')
    sys.exit(0)


def main() -> NoReturn:
    logging.basicConfig(level=logging.INFO)

    context = zmq.Context()
    socket = context.socket(zmq.REP)

    try:
        socket.bind(ZMQ_BIND_ADDRESS)
    except zmq.ZMQError as e:
        logging.error(f"Failed to bind socket: {e}")
        sys.exit(1)

    controller = Controller()

    signal.signal(signal.SIGINT, signal_handler)
    logging.info(f"Server started, waiting for messages on {ZMQ_BIND_ADDRESS}")

    dx = 1
    dy = 0
    power = 0.5
    theta = atan2(dy,dx)

    controller.process_command(theta, power, 0)
    
    try:
        while True:
            try:
                message = socket.recv_json()
                dx = message['dx']
                dy = message['dy']
                power = message['velocity']

                logging.info(f"Received message: {message}")
                theta = atan2(dy,dx)
                
                response = controller.process_command(theta, power, 0)
                socket.send_json(response)
            except Exception as e:
                logging.error(f"Error processing message: {e}")
                socket.send_json({"status": "error", "message": str(e)})
    finally:
        logging.info("Closing controller and socket...")
        controller.close()
        socket.close()
        context.term()


if __name__ == "__main__":
    main()