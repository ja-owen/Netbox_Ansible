#you need install networkscan and python-netbox modules
import networkscan
from netbox import NetBox
netbox = NetBox(host='192.168.0.130', port=80, use_ssl=False, auth_token='27172995b1a594f5ac038491dd531af73a562479')

# Main function
if __name__ == '__main__':

    # Define the network to scan
    my_network = "192.168.0.0/24"

    # Create the object
    my_scan = networkscan.Networkscan(my_network)

    # Run the scan of hosts using pings
    my_scan.run()

    # Display the IP address of all the hosts found
    for address in my_scan.list_of_hosts_found:
        print(address)
        netbox.ipam.create_ip_address(address)
