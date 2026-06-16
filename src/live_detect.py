import joblib
import pandas as pd

from datetime import datetime

from scapy.all import sniff, ARP, DNS, TCP, UDP, ICMPv6ND_NS


# Load trained model
try:
    model = joblib.load("models/anomaly_model.pkl")
    print("[+] Model loaded successfully!")
except Execption as e:
    print(f"[ERROR] Failed to load model: {e}")
    exit(1)

# Prorocol mapping
protocol_map = {

	"ARP": 0,
	"DNS": 1,
	"ICMPV6": 2,
	"MDNS": 3,
	"SSDP": 4
}

def packet_callback(packet):
    try:
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

            timestamp = datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"
            )


            alert_message = (
                f"{timestamp} | "
                f"ATTACK DETECTED | "
                f"Prorocol={protocol} | "
                f"Length={packet_length}\n"
            )

            with open("logs/alerts.log", "a") as logfile:
                logfile.write(alert_message)

            with open("reports/alerts.csv", "a") as csvfile:
                csvfile.write(
                    f"{timestamp},{protocol},{packet_length},ATTACK\n"
                )


        print("====================")

    except Exception as e:
        print(f"[ERROR] Packet processing failed: {e}")


print("[+] Starting Live AI Detection...")
print("[+] Press CTRL+C to stop\n")

try:
    sniff(
        prn=packet_callback,
        store=False
    )


except KeyboardInterrupt:
    print("\n[+] Detection stopped by user.")
