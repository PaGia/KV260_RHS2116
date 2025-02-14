from pynq import Overlay, MMIO
import pynq.lib as lib
overlay = Overlay('communication.bit')
spi = overlay.axi_quad_spi_0

def init(spi, phase=0, polarity=0):
    spi.write(0x40, 0x0a)
    spi.write(0x28, 0x04)
    spi.write(0x1c, 0)
    spi.write(0x70, 0xFFFFFFFF)
    ctrlreg = spi.read(0x60)
    ctrlreg = ctrlreg | e6
    spi.write(0x60, ctrlreg)
    ctrlreg = spi.read(0x60)
    ctrlreg = ctrlreg & ~(0x18) 
    if phase == 1:
        ctrlreg = ctrlreg | 0x10
    if polarity == 1:
        ctrlreg = ctrlreg | 0x08
    spi.write(0x60, ctrlreg)

def transfer(packet, spi):
    for data in packet:
        spi.write(0x68, data)
        spi.write(0x70, 0xFFFFFFFE)
        ctrlreg = spi.read(0x60)
        ctrlreg = ctrlreg & ~(0x100)
        spi.write(0x60, ctrlreg)
        statReg = spi.read(0x64)
        while (statReg & 0x04) == 0:
            statReg = spi.read(0x64)
        ctrlreg = spi.read(0x60)
        ctrlreg = ctrlreg | 0x100
        spi.write(0x60, ctrlreg)
    spi.write(0x70, 0xFFFFFFFF)
    recvData = list()
    RxFifoStatus = spi.read(0x64) & 0x01
    while RxFifoStatus == 0:
        temp = spi.read(0x6c)
        recvData.append(temp)
        RxFifoStatus = spi.read(0x64) & 0x01
    return recvData
init(spi)


for i in range (10):
    sendData = transfer([128+i, i*i+2], spi)
for i in range (40):
    recvData = transfer([i], spi)
    print (recvData)
    
sendData = transfer([128+5,9], spi)
recvData = transfer([128+35,9,128+37,7,128+39,9], spi)
