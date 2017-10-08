# import required modules
try:
    # Python 2 import
    from xmlrpclib import Server
except ImportError:
    # Python 3 import
    from xmlrpc.client import Server

import json
import time

# pretty printing to console
import pprint
pp = pprint.PrettyPrinter(indent=4)

REQUEST_INTERVAL = 60 * 5 # every 5 minutes

DEBUGGING = False

# Muoversi a Roma API
# load the dev key
with open("dev_key.json") as f:
    DEV_KEY = json.load(f)["key"]

# connection and authentication
s1 = Server('http://muovi.roma.it/ws/xml/autenticazione/1')
s2 = Server('http://muovi.roma.it/ws/xml/paline/7')
token = s1.autenticazione.Accedi(DEV_KEY, "")

def main():
    while True:

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
            
            print "Prossimo autobus tra: {}".format(next_bus_info["annuncio"])
        
        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    main()