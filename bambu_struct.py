from dataclasses import dataclass
import numpy as np

@dataclass
class BambuShortHdrPkt:
    bbStx:np.uint8 = 0x3D
    bbFlagWithSeq:np.uint8 = 0
    bbTLength:np.uint8 = 0
    bbCrc8:np.uint8 = 0
    bbType:np.uint8 = 0
    bbData:list[np.uint8]
    bbCrc16:np.uint16 = 0
    