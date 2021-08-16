#! /usr/bin/python3

import sys, json, os
import requests
from time import sleep

global lastNotifStatus, timeBeforeCheck, requestTimeOut, URL, headers

lastNotifStatus = False
timeBeforeCheck = 10
requestTimeOut=10
URL='https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data'
headers = {'User-Agent': 'Mozilla/7.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.39 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/539.36', 'Pragma': 'no-cache'}

# Function 
def notify(title, text):
    """
    notify("Title", "Heres an alert")
    """
    os.system("""
             osascript -e 'display notification "{}" with title "{}"'
             """.format(text, title))

def loop():
    global lastNotifStatus
    while True:
    
        try:
            myResponse = requests.get(URL, headers=headers, timeout=requestTimeOut)
            #print(myResponse.json())
            data = myResponse.json();
        except:
            print ('error')
            continue
    
        if data["status"] == True and lastNotifStatus == False:
            notify("VPN Alert [Protected]","IP: " + data["ip"] + "\nISP: "  +  data["isp"] + "\n" + data["city"] + " ," + data["country"] )
            lastNotifStatus = True
        elif data["status"] == False and  lastNotifStatus == True:
            notify("VPN Alert [Unprotected]","IP: " + data["ip"] + "\nISP : "  +  data["isp"] + "\n" + data["city"] + " ," + data["country"] )
            lastNotifStatus = False
        sleep(timeBeforeCheck)

if __name__ == "__main__":
    loop()


