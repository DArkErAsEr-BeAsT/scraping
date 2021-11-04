from scapy.all import *
from concurrent.futures import ThreadPoolExecutor
import time

Kmac = "B8:41:A4:EC:25:1E".lower()

Dmac = "E0:DC:FF:F3:4E:01".lower()

Cmac = "5C:17:CF:89:44:D7".lower()

Nmac = "80:B0:3D:0D:7E:93".lower()

def main():
    # for i in range(55):
    #     search_mac("10.0.0."+str(i))
    start_time = time.time()    
    for i in range(5):
        ls = [("10.0.0."+str(i)) for i in range(55)]
        with ThreadPoolExecutor() as exec:
            resp = exec.map(search_mac, ls)
    print("--- %s seconds ---" % (time.time() - start_time))

    d_list = []
    k_list = []
    n_list = []
    c_list = []

    for list in resp:
        d_list.append(list[0])
        n_list.append(list[1])
        c_list.append(list[2])
        k_list.append(list[3])
    with open('/home/pi/Documents/projects/projects/whosHome/tmp.txt', 'a')as f:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        f.write(current_time+'\n')
        if any(d_list):
            f.write('david is here\n')
        if any(k_list):
            f.write('kajetan is here\n')
        if any(n_list):
            f.write('nathan is here\n')
        if any(c_list):
            f.write('clement is here\n')
        f.write('\n')
def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]
    return answered_list[0][1].hwsrc 

def scan(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=5,
                              verbose=False)[0]

    clients_list = []

    for element in answered_list:
        client_dict = {"mac": element[1].hwsrc}
       
        clients_list.append(client_dict)
    mac = client_dict.get("mac")
    print(mac)
    print(ip)
   

  
def search_mac(ip):
    KAJETAN = False
    DAVID = False
    CLEMENT = False
    NATHAN = False
    mac = getmacbyip(ip)
    # print(mac)
    if mac == Dmac:
        DAVID = True
        
    if mac == Kmac:
        KAJETAN = True
        
    if mac == Cmac:
        CLEMENT = True
        
    if mac == Nmac:
        NATHAN = True
        
    l = [DAVID,NATHAN,CLEMENT,KAJETAN]
   
    return l

# print(scan('10.0.0.17'))
# print(arping('10.0.0.*'))
while True:
    main()
    time.sleep(5)