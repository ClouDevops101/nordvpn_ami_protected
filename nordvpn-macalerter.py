#! /usr/bin/python3

import sys
import json
import os
import requests
from time import sleep
from sys import platform as _platform

global lastNotifStatus, timeBeforeNextCheck, requestTimeOut, URL, headers

lastNotifStatus = False
timeBeforeNextCheck = 10
requestTimeOut = 10
URL = 'https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data'
headers = {
    'User-Agent': 'Mozilla/7.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.39 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/539.36', 'Pragma': 'no-cache'}

# Some Functions

if _platform == "linux" or _platform == "linux2":
    def notify(title, text):
        # linux
        """ 
        Ubuntu -> sudo apt-get install notify-osd  
        Debian -> sudo apt install libnotify-bin 
        Redhat/Fedora/CentOS -> yum install libnotify
        for other version please see this page https://command-not-found.com/notify-send 
        """
        os.system("""
                 notify-send "{}" "{}"
                 """.format(text, title))
elif _platform == "darwin":
    def notify(title, text):
        # MAC OS X
        os.system("""
                 osascript -e 'display notification "{}" with title "{}"'
                 """.format(text, title))

elif _platform == "win32":
    def notify(title, text):
        # Windows 32-bit
        """ 
        require installing this http://vaskovsky.net/notify-send/
        """
elif _platform == "win64":
    def notify(title, text):
        # Windows 64-bit
        """ 
        require installing this http://vaskovsky.net/notify-send/
        """
# def notify(title, text):
#     """
#     notify("Title", "Heres an alert")
#     """
#     if _platform == "linux" or _platform == "linux2":
#     # linux
#         """
#         Ubuntu -> sudo apt-get install notify-osd
#         Debian -> sudo apt install libnotify-bin
#         Redhat/Fedora/CentOS -> yum install libnotify
#         for other version please see this page https://command-not-found.com/notify-send
#         """
#         os.system("""
#                  notify-send "{}" "{}"
#                  """.format(text, title))

#     elif _platform == "darwin":
#     # MAC OS X
#         os.system("""
#                  osascript -e 'display notification "{}" with title "{}"'
#                  """.format(text, title))
#     elif _platform == "win32":
#     # Windows 32-bit
#         """
#         require installing this http://vaskovsky.net/notify-send/
#         """
#     elif _platform == "win64":
#     # Windows 64-bit
#         """
#         require installing this http://vaskovsky.net/notify-send/
#         """


def loop():
    global lastNotifStatus
    while True:

        try:
            myResponse = requests.get(
                URL, headers=headers, timeout=requestTimeOut)
            # print(myResponse.json())
            data = myResponse.json()
        except:
            #print ('error')
            notify("VPN Alert [Unknown]", "Network Error")
            lastNotifStatus = False
            sleep(timeBeforeNextCheck)
            continue

        if data["status"] == True and lastNotifStatus == False:
            notify("VPN Alert [Protected]", "IP: " + data["ip"] + "\nISP: " +
                   data["isp"] + "\n" + data["city"] + " ," + data["country"])
            lastNotifStatus = True
        elif data["status"] == False and lastNotifStatus == True:
            notify("VPN Alert [Unprotected]", "IP: " + data["ip"] + "\nISP : " +
                   data["isp"] + "\n" + data["city"] + " ," + data["country"])
            lastNotifStatus = False
        sleep(timeBeforeNextCheck)


if __name__ == "__main__":
    loop()
