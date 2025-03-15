from common import *

BambuBusPkt = []
BambuBusData = []
BambuBusTestPkt = [0x3D, 0xC5, 0x1E, 0x61, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x62, 0x66]

BambuBusIndex = 0
BambuBusFlag = 0
BambuBusLength = 0
BambuBusCrc8 = 0
BambuBusCrc16 = 0
BambuBusPktType = 0
BambuBusTargetAddr = 0
BambuBusSourceAddr = 0

def BambuBusClearVariables():
    global BambuBusLength, BambuBusIndex, BambuBusCrc8, BambuBusCrc16
    global BambuBusPktType, BambuBusTargetAddr, BambuBusSourceAddr
    global BambuBusPkt, BambuBusData

    BambuBusLength = 0
    BambuBusIndex = 0
    BambuBusCrc8 = 0
    BambuBusCrc16 = 0
    BambuBusPktType = 0
    BambuBusTargetAddr = 0
    BambuBusSourceAddr = 0
    BambuBusPkt.clear()
    BambuBusData.clear()

def BambuBusSPHandler(_in):
    global BambuBusIndex, BambuBusFlag, BambuBusLength
    ret = 1
    BambuBusPkt.append(_in)

    if BambuBusIndex == BBP_SPKT_IDX_LENGTH:
        BambuBusLength = _in
    elif BambuBusIndex == BBP_SPKT_IDX_CRC8:
        BambuBusCrc8 = _in
    elif BambuBusIndex == BBP_SPKT_IDX_TYPE:
        BambuBusPktType = _in
    else:
        if BambuBusIndex == BambuBusLength-1:
            ret = 0
        else:
            if BambuBusIndex >= BBP_SPKT_IDX_CONTENT and BambuBusIndex <= BambuBusLength - 3:
                BambuBusData.append(_in)

        if len(BambuBusPkt) > 100:
            ret = 0

    BambuBusIndex = BambuBusIndex + 1

return ret


