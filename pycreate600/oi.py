class Namespace(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

BAUD_RATE = Namespace(BAUD_300=0, BAUD_600=1, BAUD_1200=2, BAUD_2400=3, BAUD_4800=4, BAUD_9600=5, BAUD_14400=6, BAUD_19200=7, BAUD_28800=8, BAUD_38400=9, BAUD_57600=10, BAUD_115200=11, DEFAULT=11)
OPCODES = Namespace(
    RESET = 7,
    
)