# import required modules
try:
    # Python 2 import
    from xmlrpclib import Server
except ImportError:
    # Python 3 import
    from xmlrpc.client import Server

import json
import time
import serial
import os
import re
#from pyfirmata import Arduino, util

# pretty printing to console
import pprint
pp = pprint.PrettyPrinter(indent=4)


DEBUGGING = os.getenv("DEBUG") or False

# Serial communication
SERIAL_PORT = "/dev/tty.usbmodemFA131"
BAUD_RATE = 9600

# Muoversi a Roma API
REQUEST_INTERVAL = 10# minutes
# load the dev key
with open("dev_key.json") as f:
    DEV_KEY = json.load(f)["key"]

# firmata config
board = Arduino("/dev/tty.usbmodemFA131")

# led opening sequence
def opening_sequence():
    

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
# wait for arduino to be ready
time.sleep(5)
arduino.write("Starting..\n")

    print "-"*10
    print "starting.."
    print "-"*10
    # s
    for i in range(3):
        board.digital[13].write(1)
        time.sleep(0.25)
        board.digital[13].write(0)
        time.sleep(0.25)
    # o
    for i in range(3):
        board.digital[13].write(1)
        time.sleep(0.5)
        board.digital[13].write(0)
        time.sleep(0.5)
    # s
    for i in range(3):
        board.digital[13].write(1)
        time.sleep(0.25)
        board.digital[13].write(0)
        time.sleep(0.25)

# LED SEQUENCES
def init_leds():
    board.digital[13].write(0)
    board.digital[3].write(0)
    board.digital[4].write(0)
    
def bus_not_arriving():
    board.digital[4].write(1)
    board.digital[3].write(0)

def bus_far_away():
    board.digital[4].write(0)
    board.digital[3].write(0)
    
def bus_arriving():
    board.digital[4].write(0)
    board.digital[3].write(1)
    time.sleep(0.5)
    board.digital[3].write(0)
    time.sleep(0.5)
    board.digital[3].write(1)

def main():
    
    print "-"*10
    print "starting.."
    print "-"*10

    while True:

        # connection and authentication
        s1 = Server('http://muovi.roma.it/ws/xml/autenticazione/1')
        s2 = Server('http://muovi.roma.it/ws/xml/paline/7')
        token = s1.autenticazione.Accedi(DEV_KEY, "")
        result = s2.paline.Previsioni(token, "73030", "it")

        primi_arrivi = result["risposta"]["primi_per_palina"]
        if len(primi_arrivi) > 0:
            palina_info = primi_arrivi[0]["arrivi"][0]
            next_bus_info = primi_arrivi[0]["arrivi"][1]
            
            if DEBUGGING:
                print "Info palina: "
                pp.pprint(palina_info)
                print "Prossimo autobus:"
                pp.pprint(next_bus_info)
            
            # check status of bus
            if next_bus_info.has_key("annuncio"):

                if next_bus_info["annuncio"] == "In Arrivo":
                    print "86 in arrivo!"
                    bus_arriving()
                if next_bus_info["annuncio"] == "Capolinea":
                     bus_far_away()
                else:
                    print "Prossimo autobus tra: {}".format(next_bus_info["annuncio"])
                    try:
                        minutes = int(re.findall(r"(\d+)'", next_bus_info["annuncio"])[0].replace("'", ""))
                        #print "minutes: {}".format(minutes)
                        if minutes > 10:
                            bus_far_away()
                        elif minutes < 10:
                            bus_arriving()
                    except IndexError:
                        pass
            else:
                print "Nessun autobus disponibile"
                bus_not_arriving()
        
        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    #opening_sequence()
    main()