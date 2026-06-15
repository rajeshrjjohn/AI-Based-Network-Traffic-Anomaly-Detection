from  scapy.all import sniff, ARP, DNS, TCP, UDP, ICMPv6ND_NS

def packet_callback(packet):
    packet_length = len(packet)

    if packet.haslayer(ARP):
       protocol = "ARP"

    elif packet.haslayer(DNS):
       protocol = "DNS"

    elif packet.haslayer(ICMPv6ND_NS):
       protocol = "ICMPV6"

    elif packet.haslayer(TCP):
       protocol = "TCP"

    elif packet.haslayer(UDP):
       protocol = "UDP"

    else:
       protocol = "OTHER"

    print("\n--------------------")
    print(f"\nPacket Length : {packet_length}")
    print(f"Protocol        : {protocol}")
    print("--------------------")

print("[+] Starting Packet Extraction...")
print("[+] Press CTRL+C to stop\n")

sniff(prn=packet_callback, store=False)
