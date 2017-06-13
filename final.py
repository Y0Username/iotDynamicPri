from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSKernelSwitch, Controller
from mininet.node import Switch, Link, Node, OVSController, DefaultController
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel
import logging as log

CONTROLLER_IP = '127.0.0.1'
CONTROLLER_PORT = 6634
IP_BASE = '10.0.0.0/8'

def setup_topology():
        net = Mininet(topo=None, build=False, ipBase=IP_BASE, autoSetMacs=True)
        c0 = net.addController(name='c0') #, controller=Controller, ip=CONTROLLER_IP, port=CONTROLLER_PORT)

        s1 = net.addSwitch('s1') #, cls=OVSKernelSwitch)
        s2 = net.addSwitch('s2') #, cls=OVSKernelSwitch)
	s3 = net.addSwitch('s3') #, cls=OVSKernelSwitch)

        h1 = net.addHost('h1')#, ip='10.0.0.1', mac='00:00:00:00:00:01')
        h2 = net.addHost('h2')#, ip='10.0.0.2', mac='00:00:00:00:00:2')
        h3 = net.addHost('h3')#, ip='10.0.0.3', mac='00:00:00:00:00:3')
        h4 = net.addHost('h4')#, ip='10.0.0.2', mac='00:00:00:00:00:2')
        h5 = net.addHost('h5')#, ip='10.0.0.3', mac='00:00:00:00:00:3')

        l1 = net.addLink(h1, s1) #, cls=TCLink, bw=10)
        l2 = net.addLink(h2, s2) #, cls=TCLink, bw=10)
        l3 = net.addLink(h3, s2) #, cls=TCLink, bw=10)
	l4 = net.addLink(h4, s3)
	l3 = net.addLink(h5, s3)
	l4 = net.addLink(s3, s1)
	l5 = net.addLink(s2, s3)
        l4 = net.addLink(s2, s1)#, intfName1='s2-eth3') #, cls=TCLink, bw=10)

        net.build()
        net.start()
        CLI( net )
        net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    setup_topology()
