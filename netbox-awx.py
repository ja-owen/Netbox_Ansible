#!/usr/bin/env python

import json
import requests

# Netbox URL
URL = 'http://10.20.100.251'

# Netbox API Token
TOKEN = 'afc139a2f1cf2dd545f4fcb9edeebf175abbe4f4'

# AWX Filter Tags
#FILTER_TAGS = []

headers = {
    'Accept': 'application/json ; indent=4',
    'Authorization': 'Token %s' % (TOKEN),
}

device_url = URL + '/api/dcim/devices/'
devices = []
sites = {}
racks = {}
platforms = {}
tenants = {}
tags = {}
inventory = {}
hostvars = {}

# Get data from netbox

def get_data(api_url):
    out = []
    while api_url:
        api_output = requests.get(api_url, headers=headers, verify=False)
        api_output_data = api_output.json()

        if isinstance(api_output_data, dict) and "results" in api_output_data:
            out += api_output_data["results"]
            api_url = api_output_data["next"]
    return out

hosts_list = get_data(device_url)

# Filter hosts for AWX
for i in hosts_list:
    if FILTER_TAGS:
        tag_list = []
        if i['tags']:
            for tag_item in i['tags']:
                tag_list.append(tag_item['name'])
        if any(item in FILTER_TAGS for item in tag_list):
            if i['status']:
                if i['status']['label'] == 'Active':
                    devices.append(i)

    else:
        if i['status']:
            if i['status']['label'] == 'Active':
                devices.append(i)
# Populate inventory

for i in devices:
    if i['name']:
        if i['config_context']:
            hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']] = i['config_context']
        if i['site']:
            sites.setdefault(i['site']['slug'], {'hosts': []})['hosts'].append(i['name'])
            hostvars['_meta']['hostvars'][i['name']].setdefault('tags', {})['site'] = i['site']['slug']
        if i['rack']:
            racks.setdefault(i['rack']['name'], {'hosts': []})['hosts'].append(i['name'])
            hostvars['_meta']['hostvars'][i['name']].setdefault('tags', {})['rack'] = i['rack']['name']
        if i['platform']:
            platforms.setdefault(i['platform']['slug'], {'hosts': []})['hosts'].append(i['name'])
            hostvars['_meta']['hostvars'][i['name']].setdefault('tags', {})['platform'] = i['platform']['slug']
        if i['tenant']:
            tenants.setdefault(i['tenant']['slug'], {'hosts': []})['hosts'].append(i['name'])
            hostvars['_meta']['hostvars'][i['name']].setdefault('tags', {})['tenant'] = i['tenant']['slug']
        for t in i['tags']:
            tags.setdefault(t['name'], {'hosts': []})['hosts'].append(i['name'])
            hostvars['_meta']['hostvars'][i['name']].setdefault('tags', {})[t['name']] = True

inventory.update(sites)
inventory.update(racks)
inventory.update(platforms)
inventory.update(tenants)
inventory.update(tags)
inventory.update(hostvars)

print(json.dumps(inventory, indent=4))
