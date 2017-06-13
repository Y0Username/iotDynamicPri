from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch, Controller
from mininet.node import Switch, Link, Node, OVSController, DefaultController
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel
import logging as log
from OVSminiTopo import *
from configs import *
from time import sleep, time
import dynamicflow as df
import sys
import os
#client_iperfs=[]
#server_iperfs=[]

def _get_mininet_nodes(mininet,nodes):
        """
        Choose the actual Mininet Hosts (rather than just strings) that will
        be subscribers.
        :param List[str] nodes:
        :return List[Node] mininet_nodes:
        """
        return [mininet.get(n) for n in nodes]
def progress(t):
    tmp=t
    while t > 0:
        print('  %3d seconds left  \r' % (t))
        t -= 1
        sys.stdout.flush()
        if t==tmp/2:
		df.post_dynamic_flows()
	sleep(1)

    print '\r\n'


def setup_traffic_generators(mininet, EXPERIMENT_DURATION):
        """Each traffic generating host starts an iperf process aimed at
        (one of) the server(s) in order to generate random traffic and create
        congestion in the experiment.  Traffic is all UDP because it sets the bandwidth.

        NOTE: iperf v2 added the capability to tell the server when to exit after some time.
        However, we explicitly terminate the server anyway to avoid incompatibility issues."""

	internet_hosts=['h3','h6','h9','h12']
	stream_hosts=['h4','h7','h10','h13']

        internet_srv = mininet.getNodeByName('h2')
	edge_srv = mininet.getNodeByName('h1')

	switches=['s1','s2','s3','s4','s5','s6','s7']
	ports=['eth0','eth1','eth2','eth3']

	for s in switches:
	    sw=mininet.getNodeByName(s)
	    for p in ports:
	        tmp=s+"-"+p
		fn="/home/onos/iotDynamicPri/Results/"+tmp+".pcap"
		sw.popen('tcpdump -i %s -s 65535 -w %s'% (tmp, fn), shell=True)

	generators = _get_mininet_nodes(mininet, internet_hosts)
        log.info("*** Starting background traffic generators for internet")
        # We enumerate the generators to fill the range of ports so that the server
        # can listen for each iperf client.
        for n, g in enumerate(generators):
            log.info("iperf from %s to %s" % (g, internet_srv))
            # can't do self.net.iperf([g,s]) as there's no option to put it in the background
            i = internet_srv.popen('iperf3 -p %d -s > /home/onos/iotDynamicPri/Results/Internet/%s_%s.txt &' % (IPERF_INT_BASE_PORT + n, internet_srv,g), shell=True)
            #server_iperfs.append(i)
            i = g.popen('iperf3 -p %d -t %d -c %s -i %d -b %dM > /home/onos/iotDynamicPri/Results/Internet/%s.txt &' % (IPERF_INT_BASE_PORT + n, EXPERIMENT_DURATION, internet_srv.IP(), VER, INT_BAND, g), shell=True)
            #client_iperfs.append(i)


	generators = _get_mininet_nodes(mininet, stream_hosts)
        log.info("*** Starting background traffic generators for streaming")
        # We enumerate the generators to fill the range of ports so that the server
        # can listen for each iperf client.
        for n, g in enumerate(generators):
            log.info("iperf from %s to %s" % (g, edge_srv))
            # can't do self.net.iperf([g,s]) as there's no option to put it in the background
            i = edge_srv.popen('iperf3 -p %d -s > /home/onos/iotDynamicPri/Results/Stream/%s_%s.txt &' % (IPERF_ST_BASE_PORT + n, edge_srv, g), shell=True)

            #server_iperfs.append(i)
	    i = g.popen('iperf3 -p %d -t %d -u -b %dM -c %s -i %d > /home/onos/iotDynamicPri/Results/Stream/%s.txt &' % (IPERF_ST_BASE_PORT + n, EXPERIMENT_DURATION, ST_BAND, edge_srv.IP(), VER, g), shell=True)
            #client_iperfs.append(i)
	progress(EXPERIMENT_DURATION+5)
	os.system('pkill iperf3')
	os.system('pkill tcpdump')
