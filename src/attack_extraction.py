import pyshark
import pandas as pd
capture =  pyshark.FileCapture(
	'data/raw/attack_traffic.pcap',
	keep_packets=False
)

data = []

for packet in capture:
	try:
		data.append({
			"packet_length": packet.length,
			"protocol": packet.highest_layer
	})

	except:
		continue

df = pd.DataFrame(data)


print(df.head())

df.to_csv(
	'data/processed/attack_features.csv',
	index=False
)


print("CSV created sucessfully!")
