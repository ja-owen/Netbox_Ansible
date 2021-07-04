import re
import requests
import pynetbox
from netmiko import ConnectHandler
from netbox import NetBox
from pprint import pprint
from ciscoconfparse import CiscoConfParse
import time

#connection string for netbox
API_TOKEN = "869e49848b645d3b903800ab2d7325725ce1fcb7"
HEADERS = {'Authorization': f'Token {API_TOKEN}',
           'Content-Type': 'application/json', 'Accept': 'application/json'}
NB_URL = "http://192.168.0.160"
#command to cisco
command1 = 'show running-config'
command4 = 'show running-config | section interface'
command2 = 'show run | inc hostname'

def get_ip_list():
    file1 = open('c:\\temp\\hosts.txt', 'r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        time.sleep(0.5)
        s = line
        l = s.split('::')
        IP = l[1]
        device_name = get_hostname(command2, IP)
        try:
            create_device(device_name)
        except pynetbox.core.query.RequestError:
            print("Device "+device_name+" already exist")
        print(IP)
        get_interfaces_and_description(IP)

#Convert from device_name to device_ID
def request_devices(device_name):
    request_url = f"{NB_URL}/api/dcim/devices/?q={device_name}"
    devices = requests.get(request_url, headers=HEADERS)
    result = devices.json()
    print(result)
    id = result["results"][0]["id"]
    return id

def create_device(device_name):
    nb = pynetbox.api(url='http://192.168.0.160/',
                  token='869e49848b645d3b903800ab2d7325725ce1fcb7')

    result = nb.dcim.devices.create(
        name=device_name,
        device_type=4,
        device_role=6,
        site=7,
    )
    print(result)

#Send POST request
def post_interfaces(device_name, name_of_interface, description):
    id = request_devices(device_name)
    request_url = f"{NB_URL}/api/dcim/interfaces/?device={device_name}"
    interface_parameters = {
        "device": id,
        "name": name_of_interface,
        "description": description,
        "type": "virtual",
        "enabled": True,
        "mode": "access"
    }
    new_device = requests.post(
        request_url, headers=HEADERS, json=interface_parameters)
    print(new_device.json())

#connect to cisco and get config
def get_cisco_config(command1,IP):
    CONN = {
        'device_type': 'cisco_ios',
        'ip':   IP,
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco1',
        'timeout':  20
        }
    with ConnectHandler(**CONN) as conn:
        conn.enable()
        sample_config = conn.send_command(command1)
        conn.disconnect()
        return sample_config

#Get hostname
def get_hostname(command2,IP):
    conf = get_cisco_config(command2,IP)
    hostname = conf.split(' ', 1)
    return hostname[1]
    
#
#for interface we need 
#
def get_interfaces_and_description(IP):
    #load config
    conf = get_cisco_config(command4,IP)
    #regex all interfaces
    interface_pattern = re.compile(r'interface (?P<name>\S+)\n.+?\n?\s?')
    interface_match = interface_pattern.finditer(conf)
    for interfaces in interface_match:
        #print(interfaces)
        #print('%s' % (interfaces.group("name")))
        int = '%s' % (interfaces.group("name"))
        #form command for description
        command3 = "sho run interface " + int + " | inc description"
        #print(command3)
        description = get_cisco_config(command3,IP)
        delete_specchars = description.strip()
        delete_first_word = delete_specchars.split(' ', 2)
        #Get hostname from config
        hostname = get_hostname(command2,IP)
        print(hostname)
        #check if lengs of list = 2, it is means that interface has description
        if len(delete_first_word) == 2:
            post_interfaces(hostname,int,delete_first_word[1])
            print(int, delete_first_word[1])
        else:
            null = ""
            print(int)
            post_interfaces(hostname,int,null)

if __name__ == "__main__":
    get_ip_list()
