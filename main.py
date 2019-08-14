# -*- coding: utf-8 -*-
"""
main file
"""

import json
import requests

from tkinter import *

# Command line program
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
        r = requests.get(url)        
        response = json.loads(r.content)        
        print("Power Status: " + response["power"])

        if response["power"] == "standby":
            print("Action: Toggle Power Status")
            url = "http://" + ip + yapi["doPowerToggle"]
            r = requests.get(url)
            response = json.loads(r.content)        
            if response["response_code"]==0:
                print("Success")
    
            url = "http://" + ip + yapi["getStatus"]
            r = requests.get(url)        
            response = json.loads(r.content)        
            print("Power Status: " + response["power"])
    
    print("Good Bye.")

def applySettings(ip,command):
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
    print("Action: " + command)
    url = "http://" + ip + yapi[command]
    r = requests.get(url)
    response = json.loads(r.content)
    if response["response_code"]==0:
        print("Success")

# main program
if __name__ == "__main__":

    #main()

    devices = {"Staging": "192.168.86.69"}
    device  = devices["Staging"]
    print("IP: " + device)

    app = Tk()
    app.geometry("640x480")
    
    uiBApply = Button(app, text="Apply", command=applySettings(device,"getStatus"))
    uiBApply.place(x=200,y=400)
    
    app.mainloop()
