from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch
from mininet.node import Switch, Link, Node
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel
import logging as log

CONTROLLER_IP = '192.168.56.101'
CONTROLLER_PORT = 6653
IP_BASE = '10.0.0.0/8'

def setup_topology():
        """
        Builds the Mininet network, including all hosts, servers, switches, links.
        """
        net = Mininet(topo=None,
                      build=False,
                      ipBase=IP_BASE,
                      autoSetMacs=True,
                      )

        log.info('Adding controller')
        controller = net.addController(name='c0',
                                       controller=RemoteController,
                                       ip=CONTROLLER_IP,
                                       port=CONTROLLER_PORT,
                                       )

        '''
        for switch in range(1,7):
            sname = 's' + str(switch)
            log.info("Adding switch %s" % sname)
            s = net.addSwitch(sname, cls=OVSKernelSwitch)

        for host in range(1,13):
            hname = 'h' + str(host)
            log.info("Adding host %s" % hname)
            h = net.addHost(hname)

        for link in self.topo.get_links():
            from_link = link[0]
            to_link = link[1]
            log.debug("adding link from %s to %s" % (from_link, to_link))
            attributes = link[2]
            _bw = attributes.get('bw', 10)  # in Mbps
            _delay = '%fms' % attributes.get('latency', 10)
            _jitter = '1ms'
            _loss = self.error_rate

            l = self.net.addLink(self.net.get(from_link), self.net.get(to_link),
                                 cls=TCLink, bw=_bw, delay=_delay, jitter=_jitter, loss=_loss
                                 )
            self.links.append(l)
        '''

        #Adding a dummy switch for networking
        log.info("Adding standalone switch")
        s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')

        # Connecting to VM interface
        Intf('eth1', node=s1)

        log.info("Adding switch")
        s2 = net.addSwitch(sname, cls=OVSKernelSwitch)

        log.info("Adding hosts")
        h1 = net.addHost('h1')
        h2 = net.addHost('h2')

        log.info("Adding links")
        l1 = net.addLink(s2, h1,
                             cls=TCLink, bw=10
                             # , delay=_delay, jitter=_jitter, loss=_loss
                             )
        l2 = net.addLink(s2, h2,
                     	     cls=TCLink, bw=10
                             # , delay=_delay, jitter=_jitter, loss=_loss
                             )
        # Add link between the host and standalone switch
        l3 = net.addLink(h1, s1, intfName1='h1-eth1')

        # Build the network.
        log.info('Building network')
        net.build()

        # Start the switch without connecting it to controller
        net.get('s1').start([])

        # Start the network.
        log.info('Starting network')
        net.start()

        # 5. Configure the MAC address and IP address of the host interface that connects to dummy switch
        # info('*** Configure h1\'s controller communication interface\n')
        h1.cmd('ifconfig h1-eth1 hw ether 00:00:00:00:01:11')

        # info('*** Configure h1\'s IP address\n')
        h1.cmd('dhclient h1-eth1')

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
