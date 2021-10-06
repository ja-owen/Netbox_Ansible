import pynetbox
import time

#It function that connect to netbox and add devices
def adddev(dev):
    nb = pynetbox.api(url='http://192.168.0.160/',
                  token='869e49848b645d3b903800ab2d7325725ce1fcb7')

    result = nb.dcim.devices.create(
        name=dev,
        device_type=3,
        device_role=4,
        site=9,
    )
    print(result)
#Populate devices in file hosts.txt. 
#Example:
#Device1::192.168.0.1
#Device2::192.168.0.2
file1 = open('c:\\temp\\hosts.txt', 'r')
Lines = file1.readlines()
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    time.sleep(0.5)
    s = line
    l = s.split('::')
    print(l[0])
    dev = l[0]
    adddev(dev)
