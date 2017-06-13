import os

level2=['s4','s5','s6','s7']
level3=['s2','s3']
level2_link='100000000'
level2_minq='25000000'
level2_maxq='75000000'
level3_link='150000000'
level3_minq='50000000'
level3_maxq='100000000'


def add_HTB_queues(manual_links):

	for switch in level2:	
 		cmd = 'sudo ovs-vsctl set port '+switch+'-eth5 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate='+level2_link+' queues:123=@1q queues:234=@2q -- --id=@1q create queue other-config:min-rate=10000000 other-config:max-rate='+level2_minq+' -- --id=@2q create queue other-config:min-rate=20000000 other-config:max-rate='+level2_maxq
		os.system('nohup '+cmd)

	for switch in level3:	
 		cmd = 'sudo ovs-vsctl set port '+switch+'-eth5 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate='+level3_link+' queues:123=@1q queues:234=@2q -- --id=@1q create queue other-config:min-rate=10000000 other-config:max-rate='+level3_minq+' -- --id=@2q create queue other-config:min-rate=20000000 other-config:max-rate='+level3_maxq
		os.system('nohup '+cmd)

