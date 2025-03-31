from common import *

BambuBusPkt = []
BambuBusData = []
BambuBusTestShortPkt = [0x3D, 0xC5, 0x1E, 0x61, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x62, 0x66]
BambuBusTestLongPkt = [0x3d, 0x5, 0x74, 0x5, 0x10, 0x0, 0xfc, 0x0, 0x7, 0x0, 0x9, 0x3, 0x1, 0x0, 0x68, 0x75]
BambuBusIndex = 0
BambuBusFlag = 0
BambuBusLength = 0
BambuBusCrc8 = 0
BambuBusCrc16 = 0
BambuBusPktType = 0
BambuBusTargetAddr = 0
BambuBusSourceAddr = 0
BambuBusCmdId = 0
BambuBusCmdSet = 0

def BambuBusClearVariables():
    global BambuBusLength, BambuBusIndex, BambuBusCrc8, BambuBusCrc16
    global BambuBusPktType, BambuBusTargetAddr, BambuBusSourceAddr
    global BambuBusPkt, BambuBusData, BambuBusCmdId, BambuBusCmdSet

    BambuBusLength = 0
    BambuBusIndex = 0
    BambuBusCrc8 = 0
    BambuBusCrc16 = 0
    BambuBusPktType = 0
    BambuBusTargetAddr = 0
    BambuBusSourceAddr = 0
    BambuBusCmdId = 0
    BambuBusCmdSet = 0
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

def BambuBusLPHandler(_in):
    global BambuBusIndex, BambuBusFlag, BambuBusLength
    global BambuBusTargetAddr, BambuBusSourceAddr
    global BambuBusCrc8, BambuBusCrc16

    ret = 1
    BambuBusPkt.append(_in)

    if BambuBusIndex == BBP_LPKT_IDX_LENGTH:
        BambuBusLength = _in
    elif BambuBusIndex == BBP_LPKT_IDX_LENGTH + 1:
        BambuBusLength = BambuBusLength + (_in << 8)
    elif BambuBusIndex == BBP_LPKT_IDX_CRC8:
        BambuBusCrc8 = _in
    elif BambuBusIndex == BBP_LPKT_IDX_TGT_ADDR:
        BambuBusTargetAddr = _in << 8
    elif BambuBusIndex == BBP_LPKT_IDX_TGT_ADDR + 1:
        BambuBusTargetAddr = _in + BambuBusTargetAddr
    elif BambuBusIndex == BBP_LPKT_IDX_SRC_ADDR:
        BambuBusSourceAddr = _in << 8
    elif BambuBusIndex == BBP_LPKT_IDX_SRC_ADDR + 1:
        BambuBusSourceAddr = _in + BambuBusSourceAddr
    else:
        if BambuBusIndex == BambuBusLength-1:
            BambuBusCrc16 = BambuBusCrc16 + (_in << 8)
            ret = 0
        elif BambuBusIndex == BambuBusLength - 2:
            BambuBusCrc16 = _in
        else:
            BambuBusData.append(_in)

        if len(BambuBusPkt) > 100:
            ret = 0

    BambuBusIndex = BambuBusIndex + 1

    if ret == 0:
        BambuBusCmdSet = BambuBusData[2]
        BambuBusCmdId = BambuBusData[3]

        strs = f"Flag : {BambuBusPkt[1]} | Sequence : {BambuBusPkt[2] | BambuBusPkt[3] << 8} | "
        strs = strs + f"[{BAMBU_DEVICE_SET.get((BambuBusSourceAddr),f"Unknown")}({hex(BambuBusSourceAddr)})"
        strs = strs + f"-> {BAMBU_DEVICE_SET.get((BambuBusTargetAddr),f"Unknwon")}({hex(BambuBusTargetAddr)})] : "
        strs = strs + f"({BambuBusCmdSet}, {BambuBusCmdId}) : "
        strs = strs + f"{BAMBU_CMD_SET.get((BambuBusCmdSet, BambuBusCmdId), 'Unknown')} | Data : {list(map(hex,BambuBusData))}"
        print(strs)
    return ret

def BambuBusReadPacket(_in):
    global BambuBusIndex, BambuBusFlag, BambuBusLength
    ret = 1

    if BambuBusIndex == 0:
        if _in == BBP_PKT_STX:
            BambuBusIndex = 0
            BambuBusPkt.append(_in)
            BambuBusIndex = BambuBusIndex + 1
        else:
            BambuBusClearVariables()

    elif BambuBusIndex == 1:
        BambuBusFlag = _in
        BambuBusPkt.append(_in)
        BambuBusIndex = BambuBusIndex + 1
    else:
        if BambuBusFlag >= 0x80:
            ret = BambuBusSPHandler(_in)
        else:
            ret = BambuBusLPHandler(_in)
    if ret == 0:
        BambuBusClearVariables()
