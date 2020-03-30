import csv
import matplotlib.pyplot as plt

'''
note requires matplotlib
$pip install matplotlib
'''

def logger(logpath):
	num_packets = 0
	total_traffic = 0
	total_ip_traffic = 0

	talker_dict = {}
	listener_dict = {}
	application_dict = {}
	pair_dict = {}

	packet_sizes = []
	times = []
	ip_sizes = []
	ip_protocols = []
	dest_ports = []
	dests = []
	srcs = []
	input_ports = []
	output_ports = []
	in_vlans = []
	out_vlans = []
	
	pairs = []
	pairs_dict = {}

	udp_count = 0
	tcp_count = 0




	with open(logpath) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			#print(row)
			#print(row[0])
			#print(row[0],row[1],row[2],)
			srcIp = row[9]
			destIp = row[10]
			destPort = row[15] #used to find out the 

			#deal with src
			if(srcIp in talker_dict):
				talker_dict[srcIp] = talker_dict[srcIp] + 1
			else:
				talker_dict[srcIp] = 1
			
			#deal with dest
			if(destIp in listener_dict):
				listener_dict[destIp] = listener_dict[destIp] + 1
			else:
				listener_dict[destIp] = 1

			#deal with pairs
			if( (srcIp, destIp) in pair_dict):
				pair_dict[(srcIp, destIp)] = pair_dict[(srcIp, destIp)] + 1
			else:
				pair_dict[(srcIp, destIp)] = 1

			#deal with applications
			if(destPort in application_dict):
				application_dict[destPort] = application_dict[destPort] + 1
			else:
				application_dict[destPort] = 1


			#now we plot size vs time to live
			packet_size = int(row[17])
			time_to_live = int(row[13])
			ip_size = int(row[18])
			ip_protocol = int(row[11])
			input_port = int(row[2])
			output_port = int(row[3])
			in_vlan = int(float(row[7]))
			out_vlan = int(float(row[8]))

			pair = (srcIp, destIp)

			packet_sizes.append(packet_size)
			times.append(time_to_live)
			ip_sizes.append(ip_size)
			ip_protocols.append(ip_protocol)
			dest_ports.append(destPort)
			dests.append(destIp)
			srcs.append(srcIp)
			input_ports.append(input_port)
			output_ports.append(output_port)
			in_vlans.append(in_vlan)
			out_vlans.append(out_vlan)

			pairs.append(pair)
			pairs_dict[pair] = 1

			#deal with applcations

			#deal with TCP, UDP ratio
			if(ip_protocol == 6):
				tcp_count +=1
			if(ip_protocol == 17):
				udp_count +=1


			num_packets += 1
			total_traffic += int(row[17])
			total_ip_traffic += int(row[18])


	#now we find the max of  dicts--talker
	talker_list = [(k, v) for k, v in talker_dict.items()]
	talker_list.sort(key = lambda tup: tup[1], reverse = True)

	#now we find the max of  dicts--listener
	listener_list = [(k, v) for k, v in listener_dict.items()]
	listener_list.sort(key = lambda tup: tup[1], reverse = True)

	#now we find the max of  dicts--pairs
	pair_list = [(k, v) for k, v in pair_dict.items()]
	pair_list.sort(key = lambda tup: tup[1], reverse = True)

	#now we find the max of  dicts--application
	application_list = [(k, v) for k, v in application_dict.items()]
	application_list.sort(key = lambda tup: tup[1], reverse = True)

	print('Top Talkers')
	for i in range(5):
		print(str(i+1) + '. ' + str(talker_list[i]))

	print('Top Listeners')
	for i in range(5):
		print(str(i+1) + '. ' + str(listener_list[i]))

	print('Top Pairs')
	for i in range(5):
		print(str(i+1) + '. ' + str(pair_list[i]))

	print('Top application')
	for i in range(5):
		print(str(i+1) + '. ' + str(application_list[i]))

	print('Number of packets: '+ str(num_packets))
	print('Total Traffic: ' + str(total_traffic))
	print('Total IP Traffic: ' + str(total_ip_traffic))


	plt.scatter(ip_sizes, times)
	plt.title('Ip Size vs Time to Live')
	plt.xlabel('Ip Size')
	plt.ylabel('Time to Live')
	plt.show()

	plt.scatter(input_ports, output_ports)
	plt.title('Input Ports vs Output Ports')
	plt.xlabel('Input Ports')
	plt.ylabel('Output Ports')
	plt.show()





def get_dict_max(dict):
	lst = [(k, v) for k, v in dict.items()]


logger('test_SFLow_data.csv')