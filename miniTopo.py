from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch
from mininet.node import Switch, Link, Node
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel
import logging as log
from configs import *

client_iperfs=[]
server_iperfs=[]
net = Mininet(topo=None,
                      build=False,
                      ipBase=IP_BASE,
                      autoSetMacs=True,
                      )
def _get_mininet_nodes(nodes):
        """
        Choose the actual Mininet Hosts (rather than just strings) that will
        be subscribers.
        :param List[str] nodes:
        :return List[Node] mininet_nodes:
        """
        return [net.get(n) for n in nodes]

def setup_traffic_generators():
        """Each traffic generating host starts an iperf process aimed at
        (one of) the server(s) in order to generate random traffic and create
        congestion in the experiment.  Traffic is all UDP because it sets the bandwidth.

        NOTE: iperf v2 added the capability to tell the server when to exit after some time.
        However, we explicitly terminate the server anyway to avoid incompatibility issues."""

	internet_hosts=['h3','h6','h9','h12']
	stream_hosts=['h4','h7','h10','h13']        
	
        internet_srv = net.getNodeByName('h2')
	edge_srv = net.getNodeByName('h1')
	
	generators = _get_mininet_nodes(internet_hosts)
        log.info("*** Starting background traffic generators for internet")
        # We enumerate the generators to fill the range of ports so that the server
        # can listen for each iperf client.
        for n, g in enumerate(generators):
            log.info("iperf from %s to %s" % (g, internet_srv))
            # can't do self.net.iperf([g,s]) as there's no option to put it in the background
            i = g.popen('iperf -p %d -t %d -c %s &' % (IPERF_INT_BASE_PORT + n, EXPERIMENT_DURATION, internet_srv.IP()))
            client_iperfs.append(i)
            i = internet_srv.popen('iperf -p %d -t %d -s &' % (IPERF_INT_BASE_PORT + n, EXPERIMENT_DURATION))
            server_iperfs.append(i)

	generators = _get_mininet_nodes(stream_hosts)

        log.info("*** Starting background traffic generators for streaming")
        # We enumerate the generators to fill the range of ports so that the server
        # can listen for each iperf client.
        for n, g in enumerate(generators):
            log.info("iperf from %s to %s" % (g, edge_srv))
            # can't do self.net.iperf([g,s]) as there's no option to put it in the background
            i = g.popen('iperf -p %d -t %d -u -b %dM -c %s &' % (IPERF_ST_BASE_PORT + n, EXPERIMENT_DURATION, ST_BAND, edge_srv.IP()))
            client_iperfs.append(i)
            i = edge_srv.popen('iperf -p %d -t %d -u -s &' % (IPERF_ST_BASE_PORT + n, EXPERIMENT_DURATION))
            server_iperfs.append(i)


def setup_topology():
        """
        Builds the Mininet network, including all hosts, servers, switches, links.
        """
        hosts = []
        switches = []
        links = []
        

        log.info('Adding controller')
        c0 = net.addController(name='c0',
                                       controller=RemoteController,
                                       ip=CONTROLLER_IP,
                                       port=CONTROLLER_PORT,
                                       )

        # Adding a Standalone switch
        #switches[0] = net.addSwitch('s21', cls=OVSKernelSwitch, failMode='standalone')

        # Connecting the standalone switch to the interface on the machine/VM
        #Intf('eth1', node=s21)

        for switch in range(1,8):
            sname = 's' + str(switch)
            log.info("Adding switch %s" % sname)
            s = net.addSwitch(sname, cls=OVSKernelSwitch)
            switches.append(s)

        for host in range(1,15):
            hname = 'h' + str(host)
            log.info("Adding host %s" % hname)
            h = net.addHost(hname)
            hosts.append(h)

        manual_links = [['s1', 'h1', 100], ['s1', 'h2', 100], ['s1', 's2', 50 ],
                        ['s1', 's3', 50 ], ['s2', 's3', 50 ], ['s2', 's4', 50 ],
                        ['s2', 's5', 50 ], ['s3', 's6', 50 ], ['s3', 's7', 50 ],
                        ['s4', 'h3', 10 ], ['s4', 'h4', 10 ], ['s4', 'h5', 10 ],
                        ['s5', 'h6', 10 ], ['s5', 'h7', 10 ], ['s5', 'h8', 10 ],
                        ['s6', 'h9', 10 ], ['s6', 'h10',10 ], ['s6', 'h11',10 ],
                        ['s7', 'h12',10 ], ['s7', 'h13',10 ], ['s7', 'h14',10 ],
                        ]
        for link in manual_links:
            from_link = link[0]
            to_link = link[1]
            log.debug("Adding link from %s to %s" % (from_link, to_link))
            bw = link[2]
            '''
            _bw = attributes.get('bw', 10)  # in Mbps
            _delay = '%fms' % attributes.get('latency', 10)
            _jitter = '1ms'
            _loss = error_rate
            '''
            l = net.addLink(net.get(from_link), net.get(to_link),
                                   cls=TCLink, bw=bw
                                   # , delay=_delay, jitter=_jitter, loss=_loss
                                   )
            links.append(l)


        '''
        #Simple minimal topolgy code
        #TODO: move to a different file
        sname = 's' + '1'
        log.info("Adding switch %s" % sname)
        s = net.addSwitch(sname, cls=OVSKernelSwitch)

        # for host in range(1,2):
        #     hname = 'h' + str(host)
        #    log.info("Adding host %s" % hname)
        h1 = net.addHost('h1')
        h = net.addHost('h2')

        l = net.addLink('s1', 'h1',
                        cls=TCLink, bw=10
                        # , delay=_delay, jitter=_jitter, loss=_loss
                        )
        l1 = net.addLink('s1', 'h2',
                     	cls=TCLink, bw=10
                        # , delay=10ms, jitter=1ms, loss=error_rate
                        )
        '''

        # Build the network
        log.info('Building network')
        net.build()  	
	
        # Start the network
        log.info('Starting network')
        net.start()
	net.pingAll()
	#Starting the internet and stream traffic
	setup_traffic_generators()
        # Drop the user in to a CLI so user can run commands.
        CLI( net )

        # After the user exits the CLI, shutdown the network.
        log.info('Stopping network')
        net.stop()



if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    setup_topology()
    
    #generators = _get_mininet_nodes(12)
    #print(generators)

# Allows the file to be imported using `mn --custom <filename> --topo minimal`
# topos = {
#     'minimal': MinimalTopo
# }
