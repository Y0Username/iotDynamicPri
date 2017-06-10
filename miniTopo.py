from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch
from mininet.node import Switch, Link, Node
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel
import logging as log

CONTROLLER_IP = '192.168.56.101'
CONTROLLER_PORT = 6653

def setup_topology():
        """
        Builds the Mininet network, including all hosts, servers, switches, links.
        """
        hosts = []
        switches = []
        links = []
        net = Mininet(topo=None,
                      build=False,
                      # ipBase=IP_SUBNET,
                      # autoSetMacs=True,
                      )

        log.info('Adding controller')
        controller = net.addController(name='c0',
                                       controller=RemoteController,
                                       ip=CONTROLLER_IP,
                                       port=CONTROLLER_PORT,
                                       )

        for switch in range(1,7):
            sname = 's' + str(switch)
            log.info("Adding switch %s" % sname)
            s = net.addSwitch(sname, cls=OVSKernelSwitch)
            switches.append(s)

        for host in range(1,14):
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
        for link in manual_links():
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
                                   cls=TCLink, bw=_bw
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

        # Drop the user in to a CLI so user can run commands.
        CLI( net )

        # After the user exits the CLI, shutdown the network.
        log.info('Stopping network')
        net.stop()

if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    setup_topology()

# Allows the file to be imported using `mn --custom <filename> --topo minimal`
# topos = {
#     'minimal': MinimalTopo
# }
