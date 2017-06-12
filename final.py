from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch
from mininet.node import Switch, Link, Node
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel
import logging as log

CONTROLLER_IP = '192.168.56.101'
CONTROLLER_PORT = 6653
IP_BASE = '10.0.5.0/24'

def setup_topology():
        net = Mininet(topo=None, build=False, ipBase=IP_BASE, autoSetMacs=True)
        c0 = net.addController(name='c0', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT)

        s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
        s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

        h1 = net.addHost('h1', ip='10.0.5.1', mac='00:00:00:00:00:01')
        h2 = net.addHost('h2', ip='10.0.5.2', mac='00:00:00:00:00:2')

        l1 = net.addLink(h1, s1, cls=TCLink, bw=10)
        l2 = net.addLink(h2, s2, cls=TCLink, bw=10)
        l3 = net.addLink(s1, s2, cls=TCLink, bw=5)
        l4 = net.addLink(s1, s2, cls=TCLink, bw=5)

        net.build()
        net.start()

        CLI( net )

        log.info('Stopping network')
        net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    setup_topology()
