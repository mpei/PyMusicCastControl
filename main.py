# -*- coding: utf-8 -*-
"""
main file
"""

import argparse
import ipaddress
import json
import logging
import netifaces
import psutil
import requests
import socket
import tkinter as tk

def getHostnameIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = socket.gethostname()
    try:
        s.connect(('85.25.139.4', 1))        
        IP = s.getsockname()[0]
    except:
        logging.error("Could not determine host IP address. Falling back to 127.0.0.1.")
        IP = '127.0.0.1'
    finally:
        s.close()
    return hostname, IP

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
        logging.debug("Success. IP: " + ip + " Command: " + url)

def getIPfromNIC(interface):
    ip = netifaces.ifaddresses(interface)
    logging.debug("Interface: " + interface + " IP: " + ip)
    return ip

# Command line program
def initCmd():

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

# Tk programm
def initTk():
    
    app = tk.Tk()
    app.geometry("640x480")
    
    networkInterfaces=netifaces.interfaces()
    selectedInterface=tk.StringVar(app)
    selectedInterface.set(networkInterfaces[0])
    uiDropDownInterfaces = tk.OptionMenu(app, selectedInterface, *networkInterfaces, command=getIPfromNIC)
    uiDropDownInterfaces.place(x=50,y=50)

    variable = tk.StringVar(app)
    variable.set("one") # default value
    uiDropDownDevices = tk.OptionMenu(app, variable, "one", "two", "three")
    uiDropDownDevices.place(x=50,y=100)
    
    uiBApply = tk.Button(app, text="Apply", command=applySettings(device,"getStatus"))
    uiBApply.place(x=200,y=400)
    
    app.mainloop()
    

# main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-t","--guitk", help="Tkinter GUI", action="store_true")
    parser.add_argument("-q","--guiqt", help="Qt GUI not implemented", action="store_true")
    parser.add_argument("-v","--verbosity", help="increase output verbosity", action="store_true")

    logging.basicConfig(filename='PyMusicCast.log', filemode='w', 
                        format='%(levelname)s - %(message)s', level=logging.DEBUG)
    logging.warning('This is a Warning')
    logging.info('Admin logged in')

    args = parser.parse_args()
    
    host_name, host_ip = getHostnameIP()
    logging.info("Hostname: " + host_name)
    logging.info("Host IP : " + host_ip)
    
    devices = {"Staging": "192.168.86.69"}
    device  = devices["Staging"]
    logging.debug("IP: " + device)
    
    if (args.guitk):
        logging.debug("Tkinter GUI requested.")
        initTk()
    else:
        initCmd()

