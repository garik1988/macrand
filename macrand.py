#! usr/bin/env python
import subprocess
import sys

from randmac import RandMac
from optparse import OptionParser
import re




def generate_mac(): #random mac address generator

    example_mac = "00:00:00:00:00:00"

    generated_mac = RandMac(example_mac, True)

    return str(generated_mac)

def list_interfaces(): #returns a list with interfaces

    ifconfig_output = subprocess.check_output(["ifconfig"]).decode("utf-8") #creates multine string from ifconfig output in utf-8 encoding

    interfaces = re.findall(r"^\w+", ifconfig_output, re.MULTILINE) #makes a list of available interfaces

    interfaces.remove("lo") #removes loopback interface from list

    return interfaces

def print_interfaces():

    interfaces=list_interfaces()

    for i in range(len(interfaces)):  # prints available interfaces

        print(str(i) + ")", interfaces[i], "\n")

def check_interface(interface): #checks if user's entered interface exists if not lists availamble interfaces

    interfaces=list_interfaces()

    if  interface  in interfaces: #checks if user's entered interface exists
        change_mac(interface)

    else:

        print ("+ There is no such interface available")


def ifconfig_output_capture_mac(interface): #captures current mac address of interface

    ifconfig_output = subprocess.check_output(["ifconfig", interface]).decode("utf-8")

    current_mac = re.findall(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output, re.MULTILINE)

    return current_mac[0]

def change_mac(interface):

    if interface=="lo": 
        print("[-] lo is loopback interface, it dosen't have a mac address choose another interface")
    else:

        new_mac=generate_mac()

        print ("+ Changing Mac Address for "+interface+" to "+new_mac)

        if new_mac == ifconfig_output_capture_mac(interface): #checks if the new random mac is different from the one trying to change if it is its generates new one

            new_mac = generate_mac()

            subprocess.call("ifconfig " + interface + " down", shell=True)

            subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)

        elif new_mac != ifconfig_output_capture_mac(interface):

            subprocess.call("ifconfig " + interface + " down", shell=True)

            subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
        subprocess.call("ifconfig " + interface + " up", shell=True)

        if new_mac == ifconfig_output_capture_mac(interface) :

            print("+ Mac address changed succesfully to"+new_mac)
        else:

            print ("- Mac address failed to change")




def get_arguments():

    parser = OptionParser()

    parser.add_option("-i", "--interface" , dest = "interface" , help = "Interface to change its MAc address")

    parser.add_option("-s", "--show" , action = "store_true", dest = "show", help = "show available interfaces")

    (options, args) = parser.parse_args()

    if options.interface:
        check_interface(options.interface)

    if options.show==True:
        print_interfaces()

    return options



options=get_arguments()

