# -*- coding: utf-8 -*-
"""
main file
"""

import json
import requests

def main():

    # greeting
    version="0.1"
    print("Python MusicCast Control - Version: " + version)
    
    # keep hardcoded list of devices here for now
    # this needs to be sniffed over the network later
    devices = {"Staging": "192.168.86.69"}
    
    yapi = {"getStatus": "/YamahaExtendedControl/v1/main/getStatus",
           "doPowerOn": "/YamahaExtendedControl/v1/main/setPower?power=on",
           "doStandBy": "/YamahaExtendedControl/v1/main/setPower?power=sta",
           "doPowerToggle": "/YamahaExtendedControl/v1/main/setPower?power=toggle",
           "doSetSleepTimer": "http://192.168.5.219/YamahaExtendedControl/v1/main/setSleep?sleep=60",
           "doCancelSleepTimer": "http://192.168.5.219/YamahaExtendedControl/v1/main/setSleep?sleep=0",
           "setBluetooth":  "/YamahaExtendedControl/v1/main/setInput?input=bluetooth",
           "doVolumeUp" : "/YamahaExtendedControl/v1/main/setVolume?volume=up",
           "doVolumeDown" : "/YamahaExtendedControl/v1/main/setVolume?volume=down"
           }
    
    print("Getting status of devices: ")
    
    for device, ip in devices.items():
        print("Device: " + device + " IP: " + ip)
        
        url = "http://" + ip + yapi["getStatus"]
        #print(url)
        r = requests.get(url)
        #print(r.content)
        
        response = json.loads(r.content)
        
        print("Power Status: " + response["power"])

#        url = "http://" + ip + yapi["doPowerOn"]
#        print(url)
#        r = requests.get(url)
#        print(r.content)
    
    print("Good Bye.")

if __name__ == "__main__":
    main()
