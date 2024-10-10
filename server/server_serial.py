import time

import zmq
import signal
import sys
import os
import logging
from typing import NoReturn

from controller import Controller
from constants import ZMQ_BIND_ADDRESS


def signal_handler(sig, frame):
    print('Shutting down server...')
    sys.exit(0)


def main() -> NoReturn:

    SERIAL_PORT : str = os.getenv('SERIAL_PORT')
    logging.basicConfig(level=logging.INFO)

    context = zmq.Context()
    socket = context.socket(zmq.REP)

    try:
        socket.bind(ZMQ_BIND_ADDRESS)
    except zmq.ZMQError as e:
        logging.error(f"Failed to bind socket: {e}")
        sys.exit(1)

    controller = Controller(SERIAL_PORT)

    signal.signal(signal.SIGINT, signal_handler)
    logging.info(f"Server started, waiting for messages on {ZMQ_BIND_ADDRESS}")

    try:
        while True:
            try:
                message = socket.recv_json()
                logging.info(f"Received message: {message}")

                response = controller.process_command(message)
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