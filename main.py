
#!/usr/bin/env python

import time
import serial
import os
from common import * 
from bambu import *
from bambu_interface import *

devName = '/dev/ttyUSB0'
bambuSerial = BambuSerial(devName)

if __name__ == "__main__":
    bambuSerial.open()
    while True:
        (ret, pkt) = bambuSerial.getMessage()
        if ret == 0:
            print(f"(ret = {ret} / pkt : {pkt})")
            bambuSerial.clear()
        #strs = int.from_bytes(ser.read())
        #BambuBusReadPacket(strs)
