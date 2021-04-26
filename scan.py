#!/usr/bin/python3


import subprocess
import time
import argparse
import sys


parser = argparse.ArgumentParser(description='Scan for APs offline and determine location when you\'re online.')
parser.add_argument('--scan', action='store_true', help='[Offline] Scan for MAC addresses of APs in range to determine your location.')
parser.add_argument('--location', action='store_true', help='[Online] Determine locations based on scanned APs.')
args = parser.parse_args()

def getMacs():
    cmd = """sudo iw dev wlan0 scan | grep \"on wlan0\" | awk \'{print $2}\' | cut -d \"(\" -f1 | awk \'$0=\"{ \\"mac\\": \\"\"$0\' | sed -e \'s/$/\\" },/\' | sed \'$ s/,$//g\' | tr -d '\n' """
    output = subprocess.getoutput(cmd)

    print(output)
    with open('macs.txt', 'a') as f:
        f.write(output + "\n")


def getLocation(mac):
    apikey = "ENTER API KEY HERE"
    cmd = "curl -s -X POST 'https://positioning.hereapi.com/v2/locate?apiKey="+ apikey + "' -H 'Content-Type: application/json' -d '{ \"wlan\": [" + mac + "] }'"

    output = subprocess.getoutput(cmd)
    print(output)


if args.scan == args.location:
    print("Please use --scan or --location")
    sys.exit()
elif args.scan:
    # Reset macs file
    with open('macs.txt', 'w') as document: pass

    print("Scanning for APs every 10 seconds...")
    for i in range(200):
        time.sleep(10)
        getMacs()
elif args.location:
    print("Getting the locations...")
    with open('macs.txt', 'r') as f:
        macs = f.readlines()
        for mac in macs:
            if not "failed" in mac:
                time.sleep(3)
                getLocation(mac)



