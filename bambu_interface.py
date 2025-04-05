import serial

def parseBambuBus(pkt):
    return 0

class BambuInterface:
    def open(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
    
    def clear(self):
        raise NotImplementedError
    
    def getMessage(self):
        raise NotImplementedError
    
class BambuSerial(BambuInterface):

    def __init__(self, devName):
        self.devName = devName
        self.serialDev = None
        self.bambuPkt = []

    def open(self):
        self.serialDev = serial.Serial(port=self.devName,baudrate=1228800, parity=serial.PARITY_EVEN, timeout=1)
        
    def close(self):
        if self.serialDev:
            self.serialDev.close()
    
    def clear(self):
        self.bambuPkt.clear()
        
    def getMessage(self):
        ret = self._readBambuBusFromSerial()
        
        return (ret, self.bambuPkt) #(ret, parseBambuBus(self.bambuPkt))
    
    def _readBambuBusFromSerial(self):
        ret = 1
        totalLength = 0

        r = int.from_bytes(self.serialDev.read())

        if r == 0x3D:
            # Store STX
            self.bambuPkt.append(r)
            
            # Store Flag
            f = int.from_bytes(self.serialDev.read())
            self.bambuPkt.append(f)

            # Store totalLength 1 byte
            r = int.from_bytes(self.serialDev.read())
            self.bambuPkt.append(r)
            totalLength = r

            # Long Header Packet
            if f < 0x80:
                # Store totalLength 1 more byte
                r = int.from_bytes(self.serialDev.read())
                self.bambuPkt.append(r)
                totalLength = totalLength + (r << 8)
                
            while totalLength != 0:
                r = int.from_bytes(self.serialDev.read())
                self.bambuPkt.append(r)
                totalLength = totalLength - 1

            ret = 0
        else:
            ret = 1

        return ret

    
