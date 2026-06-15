import os
import joblib
import pandas as pd

MODEL_PATH = "models/anomaly_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("[+] Model loaded successfully!")
except FileNotFoundError:
    print(f"[ERROR] Model file not found: {MODEL_PATH}")
    exit(1)
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")
    exit(1)

protocol_map = {

    "ARP": 0,
    "DNS": 1,
    "ICMPV6": 2,
    "MDNS": 3,
    "SSDP": 4
 }

while True:
    try:
        packet_length = int(input("\nEnter Packet Length: "))

        if packet_length <= 0:
            print("[!] Packet length must be positive.")
            continue

        protocol = input("Enter Protocol: ").strip().upper()

        if protocol not in protocol_map:
            print(f"[!] Unkown Protocol! Valid options: {list(protocol_map.keys())}")
            continue


        data = pd.DataFrame(
            [[packet_length, protocol_map[protocol]]],
            columns=["packet_length", "protocol"]
        )

        prediction = model.predict(data)

        print("Raw Prediction:", prediction)

        if prediction[0] == 0:
            print("[+] NORMAL TRAFFIC")
        else:
            print("[!] ATTACK DETECTED")

    except ValueError as e:
        print(f'[VALUE ERROR] {e}')

    except KeyboardInterrupt:
        print("\nExiting Dectection System...")
        break

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
