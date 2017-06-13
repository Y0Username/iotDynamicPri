from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch
from mininet.node import Switch, Link, Node
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel
import logging as log
from subprocess import Popen, PIPE
import os
import add_queues
import data_flows as df
from configs import *

LEVEL_1_BW=100
LEVEL_2_BW=100
LEVEL_3_BW=150
LEVEL_4_BW=300

net = Mininet(topo=None,
                      build=False,
                      ipBase=IP_BASE,
                      autoSetMacs=True,
                      )

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

	# Connecting to VM interface
        Intf('eth2', node=switches[0])

        for host in range(1,15):
            hname = 'h' + str(host)
            log.info("Adding host %s" % hname)
            h = net.addHost(hname, ip=IP_PREFIX+str(host), mac=MAC_PREFIX+str(host))
            hosts.append(h)

        manual_links = [['s1', 'h1', LEVEL_4_BW], ['s1', 'h2', LEVEL_4_BW], ['s1', 's2', 3 ],
                        ['s1', 's3', 3 ], #['s2', 's3', 0 ], 
			['s2', 's4', 2 ],
                        ['s2', 's5', 2 ], ['s3', 's6', 2 ], ['s3', 's7', 2 ],
                        ['s4', 'h3', LEVEL_1_BW ], ['s4', 'h4', LEVEL_1_BW ], ['s4', 'h5', LEVEL_1_BW ],
                        ['s5', 'h6', LEVEL_1_BW ], ['s5', 'h7', LEVEL_1_BW ], ['s5', 'h8', LEVEL_1_BW ],
                        ['s6', 'h9', LEVEL_1_BW ], ['s6', 'h10',LEVEL_1_BW ], ['s6', 'h11',LEVEL_1_BW ],
                        ['s7', 'h12',LEVEL_1_BW ], ['s7', 'h13',LEVEL_1_BW ], ['s7', 'h14',LEVEL_1_BW ]]
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
	    if bw not in [2,3]:
            	l = net.addLink(net.get(from_link), net.get(to_link),
                                   cls=TCLink, bw=bw
                                   # , delay=_delay, jitter=_jitter, loss=_loss
                                   )
            	links.append(l)
	    else:
		l = net.addLink(link[0], link[1], intfName2=link[1]+'-eth5')
		links.append(l)
	

    	# Link for internet
    	l = net.addLink('h1', 's1', intfName1='h1-eth1')
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

	# info('*** Configure h1\'s controller communication interface\n')
        hosts[0].cmd('ifconfig h1-eth1 hw ether 00:00:00:00:01:11')

        # info('*** Configure h1\'s IP address\n')
        #hosts[0].cmd('dhclient h1-eth1')

	# Adding links with Queues with Linux HTB
	add_queues.add_HTB_queues()
    	
	net.pingAll()
    	#Starting the internet and stream traffic
    	df.setup_traffic_generators(net)

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
