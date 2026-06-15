import pyshark

capture = pyshark.LiveCapture(interface='enp0s3')

for packet in capture.sniff_continuously(packet_count=10):

	print(packet)
