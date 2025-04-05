from dataclasses import dataclass, field
import numpy as np

@dataclass
class BambuShortHdrPkt:
    bbStx:np.uint8 = 0x3D
    bbFlagWithSeq:np.uint8 = 0
    bbTLength:np.uint8 = 0
    bbCrc8:np.uint8 = 0
    bbType:np.uint8 = 0
    bbData:list[np.uint8] = field(default_factory=list)
    bbCrc16:np.uint16 = 0

@dataclass
class BambuLongHdrPkt:
    bbStx:np.uint8 = 0x3D
    bbFlag:np.uint8 = 0
    bbPktSeq:np.uint16 = 0
    bbTLength:np.uint16 = 0
    bbCrc8:np.uint8 = 0
    bbTargetAddr:np.uint16 = 0
    bbSourceAddr:np.uint16 = 0
    bbData:list[np.uint8] = field(default_factory=list)
    bbCrc16:np.uint16 = 0
