import joblib
import pandas as pd

from scapy.all import sniff, ARP, DNS, TCP, UDP, ICMPv6ND_NS


# Load trained model
model = joblib.load("models/anomaly_model.pkl")

print("[+] Model loaded successfully!")


protocol_map = {

	"ARP": 0,
	"DNS": 1,
	"ICMPV6": 2,
	"MDNS": 3,
	"SSDP": 4
}

def packet_callback(packet):

    packet_length = len(packet)

	# Detect protocol
    if packet.haslayer(ARP):
        protocol = "ARP"

    elif packet.haslayer(DNS):
        protocol = "DNS"

    elif packet.haslayer(ICMPv6ND_NS):
        protocol = "ICMPV6"

    else:
        return


	# Create dataframe for prediction
    data = pd.DataFrame(
        [[packet_length, protocol_map[protocol]]],
        columns=["packet_length", "protocol"]
    )
	# Predict

    predicition = model.predict(data)

    print("\n====================")
    print(f"Packet Length : {packet_length}")
    print(f"Protocol      : {protocol}")

    if predicition[0] == 0:
        print("[+] NORMAL TRAFFIC")
    else:
        print("[!] ATTACK DETECTED")

    print("====================")

print("[+] Starting Live AI Detection...")
print("[+] Press CTRL+C to stop\n")

sniff(prn=packet_callback, store=False)
