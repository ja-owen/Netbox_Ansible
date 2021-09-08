import requests
import json
API_TOKEN = "869e49848b645dew34ww2d7325725ce1fcb7"
HEADERS = {'Authorization': f'Token {API_TOKEN}', 'Content-Type': 'application/json','Accept': 'application/json'}
NB_URL = "http://192.168.0.16"

device_name = "R4"
name_of_interface = "Ethernet0/1"
description = "Myine clyaine"
#convert device_name to device_id 
def request_devices(device_name):
    request_url = f"{NB_URL}/api/dcim/devices/?q={device_name}"
    devices = requests.get(request_url, headers = HEADERS)
    result = devices.json()
    id = result["results"][0]["id"]
    return id
    print(result["results"][0]["id"])
#Send POST request    
def post_interfaces(device_name,name_of_interface):
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
    
    new_device = requests.post(request_url, headers = HEADERS, json=interface_parameters)
    print(new_device.json())
    
post_interfaces(device_name,name_of_interface)
