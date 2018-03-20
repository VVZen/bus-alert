# -*- coding:  utf8 -*-
import time
import serial
import sys
import glob

def list_serial_ports():
    '''
    List serial port names
    '''

    # check current OS
    if sys.platform.startswith("win"):
        ports = ["COM{}".format(i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsopported platform")
    
    # add available ports
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print "Serial ports available:\n\t{}".format("\n\t".join(result))

if __name__ == "__main__":
    list_serial_ports()