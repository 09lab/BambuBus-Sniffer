
#!/usr/bin/env python

import time
import serial
import os
from common import * 
from bambu import *

ser = serial.Serial(port='/dev/ttyUSB0',baudrate =1228800, parity=serial.PARITY_EVEN, timeout=1)

if __name__ == "__main__":
    while True:
        strs = int.from_bytes(ser.read())
        print("0x%02X " % strs)
        BambuBusReadPacket(strs)
