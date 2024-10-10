from typing import Final

# Serial communication settings
SERIAL_BAUDRATE: Final[int] = 38400
SERIAL_TIMEOUT: Final[float] = 1.0

# Controller settings
DEVICE_ID: Final[int] = 0xa8
MESSAGE_LENGTH: Final[int] = 20  # 15 + 5
MESSAGE_ID: Final[int] = 1
MAX_FREQ: Final[int] = 20000

# CRC settings
CRC_POLYNOMIAL: Final[int] = 0x18005
CRC_INITIAL: Final[int] = 0xFFFF
CRC_XOR_OUT: Final[int] = 0x0000

# ZeroMQ settings
ZMQ_BIND_ADDRESS: Final[str] = "tcp://*:5555"