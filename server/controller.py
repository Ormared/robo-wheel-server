import math
import logging
from typing import Dict, Tuple

import crcmod
import serial

from constants import (
    SERIAL_PORT, SERIAL_BAUDRATE, SERIAL_TIMEOUT,
    DEVICE_ID, MESSAGE_LENGTH, MESSAGE_ID, MAX_FREQ,
    CRC_POLYNOMIAL, CRC_INITIAL, CRC_XOR_OUT
)


class Controller:
    def __init__(self, port: str = SERIAL_PORT, baudrate: int = SERIAL_BAUDRATE):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=SERIAL_TIMEOUT)
        except serial.SerialException as e:
            logging.error(f"Failed to open serial port: {e}")
            raise

        self.crc16_modbus = crcmod.mkCrcFun(CRC_POLYNOMIAL, rev=True, initCrc=CRC_INITIAL, xorOut=CRC_XOR_OUT)

    # def process_command(self, command: Dict[str, float]) -> Dict[str, str]:
    def process_command(self, theta, power, turn) -> Dict[str, str]:
        # theta = command.get('theta', 0)
        # power = command.get('power', 0)
        # turn = command.get('turn', 0)

        motor_freqs = self._calculate_frequencies(theta, power, turn)
        try:
            self._move(*motor_freqs)
        except Exception as e:
            logging.error(f"Failed to move: {e}")
            return {"status": "error", "message": str(e)}

        return {"status": "success"}

    def _calculate_frequencies(self, theta: float, power: float, turn: float) -> Tuple[int, int, int, int]:
        sin = math.sin(theta - math.pi / 4)
        cos = math.cos(theta - math.pi / 4)
        max_ = max(abs(sin), abs(cos))

        MotorAFreq = power * cos / max_ + turn
        MotorBFreq = power * sin / max_ - turn
        MotorCFreq = power * sin / max_ + turn
        MotorDFreq = power * cos / max_ - turn

        if power + abs(turn) > 1:
            scale = power + abs(turn)
            MotorAFreq /= scale
            MotorBFreq /= scale
            MotorCFreq /= scale
            MotorDFreq /= scale

        MotorAFreq = round(MotorAFreq * MAX_FREQ)
        MotorBFreq = round(MotorBFreq * MAX_FREQ)
        MotorCFreq = round(MotorCFreq * MAX_FREQ)
        MotorDFreq = round(MotorDFreq * MAX_FREQ)

        return MotorAFreq, MotorBFreq, MotorCFreq, MotorDFreq

    def _move(self, MotorAFreq: int, MotorBFreq: int, MotorCFreq: int, MotorDFreq: int) -> None:
        message = [
            DEVICE_ID, MESSAGE_LENGTH, MESSAGE_ID,
            0, 0, 0, 0,
            MotorAFreq >> 8 & 0xff, MotorAFreq & 0xff,
            MotorBFreq >> 8 & 0xff, MotorBFreq & 0xff,
            MotorCFreq >> 8 & 0xff, MotorCFreq & 0xff,
            MotorDFreq >> 8 & 0xff, MotorDFreq & 0xff,
            0, 0, 0
        ]
        crc = self.crc16_modbus(bytearray(message))
        crc_bytes = crc.to_bytes(2, byteorder='little')
        message.extend(crc_bytes)

        self.ser.write(bytearray(message))
        response = self.ser.read(34 + 5)
        response_hex_array = [hex(b) for b in response]
        logging.debug(f"Response: {response_hex_array}")

    def close(self) -> None:
        self.ser.close()
