import time
import serial

SERIAL_PORT = "/dev/tty.usbmodemFA131"
BAUD_RATE = 9600

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
# wait for arduino to be ready
time.sleep(5)
arduino.write("Starting..\n")

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