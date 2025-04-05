import serial
from common import *
from bambu_struct import *

def parseBambuBus(pkt):
    ret = None

    if pkt[BBP_PKT_IDX_FLAG] > 0x80:
        bbpFlag = pkt[BBP_PKT_IDX_FLAG]
        bbpLength = pkt[BBP_SPKT_IDX_LENGTH]
        bbpType = pkt[BBP_SPKT_IDX_TYPE]
        bbpData = pkt[BBP_SPKT_IDX_CONTENT:-2]
        bbpCrc8 = pkt[BBP_SPKT_IDX_CRC8]
        bbpCrc16 = pkt[-2:]

        ret = BambuShortHdrPkt(0x3D,bbpFlag, bbpLength, bbpCrc8,
            bbpType, bbpData, bbpCrc16)
    else:
        bbpFlag = pkt[BBP_PKT_IDX_FLAG]
        bbpSeq = pkt[BBP_PKT_IDX_FLAG+1]
        bbpLength = pkt[BBP_LPKT_IDX_LENGTH] + (pkt[BBP_LPKT_IDX_LENGTH+1] << 8)
        bbpTgtAddr = pkt[BBP_LPKT_IDX_TGT_ADDR] + (pkt[BBP_LPKT_IDX_TGT_ADDR+1] << 8)
        bbpSrcAddr = pkt[BBP_LPKT_IDX_SRC_ADDR] + (pkt[BBP_LPKT_IDX_SRC_ADDR+1] << 8)
        bbpData = pkt[BBP_LPKT_IDX_CONTENT:-2]
        bbpCrc8 = pkt[BBP_LPKT_IDX_CRC8]
        bbpCrc16 = pkt[-2:]

        ret = BambuLongHdrPkt(0x3D, bbpFlag, bbpSeq, bbpLength, bbpCrc8,
            bbpTgtAddr, bbpSrcAddr, bbpData, bbpCrc16)
    return ret

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
        self.bambuData = []

    def open(self):
        self.serialDev = serial.Serial(port=self.devName,baudrate=1228800, parity=serial.PARITY_EVEN, timeout=1)
        
    def close(self):
        if self.serialDev:
            self.serialDev.close()
    
    def clear(self):
        self.bambuPkt.clear()
        
    def getMessage(self):
        ret = self._readBambuBusFromSerial()
        
        if ret == 0:
            return (ret, parseBambuBus(self.bambuPkt))
        else:
            return (ret, None)
    
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
            totalLength = r-3

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

    
