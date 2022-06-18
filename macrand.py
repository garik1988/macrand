#! usr/bin/env python
import subprocess
from randmac import RandMac
from get_nic import getnic
from optparse import OptionParser




def generate_mac(): #random mac address generator

    example_mac = "00:00:00:00:00:00"

    generated_mac = RandMac(example_mac, True)

    return str(generated_mac)

def check_interface(interface): #checks if user's entered interface exists if not lists availamble interfaces
    interfaces = getnic.interfaces() #makes a list of availamble interfaces

    if interface not in interfaces: #checks if user's entered interface exists
        print ("+ There is no such interface available")
        print("Available Interfaces: \n")
        for i in range(len(interfaces)):  # prints available interfaces
            print(str(i) + ")", interfaces[i], "\n")
    else:
        change_mac(interface)

def change_mac(interface):
        new_mac=generate_mac()

        print ("+ Changing Mac Address for "+interface+" to "+new_mac)

        subprocess.call("ifconfig " + interface + " down", shell=True)

        subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)

        subprocess.call("ifconfig " + interface + " up", shell=True)
        
def get_arguments():
    parser = OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAc address")

    (options, args) = parser.parse_args()

    check_interface(options.interface)

    return options



options=get_arguments()
