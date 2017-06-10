from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch
from mininet.node import Switch, Link, Node
from mininet.cli import CLI
from mininet.link import TCLink, Intf

CONTROLLER_IP = '192.168.56.101'
CONTROLLER_PORT = 6653

def setup_topology():
        """
        Builds the Mininet network, including all hosts, servers, switches, links.
        """
        net = Mininet(topo=None,
                           build=False,
                           ipBase=IP_SUBNET,
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

        sname = 's' + '1'
        log.info("Adding switch %s" % sname)
        s = net.addSwitch(sname, cls=OVSKernelSwitch)

        for host in range(1,2):
            hname = 'h' + str(host)
            log.info("Adding host %s" % hname)
            h = net.addHost(hname)

        l = net.addLink('s1', 'h1',
                             cls=TCLink, bw=10
                             # , delay=_delay, jitter=_jitter, loss=_loss
                             )
        l = net.addLink('s1', 'h2',
                     cls=TCLink, bw=10
                     # , delay=_delay, jitter=_jitter, loss=_loss
                     )

        log.info('Starting network')

        # Build the network
        net.build()

        # Start the network
        net.start()

        # Drop the user in to a CLI so user can run commands.
        CLI( net )

        # After the user exits the CLI, shutdown the network.
        net.stop()

if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    setup_topology()

# Allows the file to be imported using `mn --custom <filename> --topo minimal`
# topos = {
#     'minimal': MinimalTopo
# }
