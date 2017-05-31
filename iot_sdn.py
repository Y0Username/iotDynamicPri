"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        edgeServer = self.addHost( 'h1' )
        Host1 = self.addHost( 'h2' )
        Host2 = self.addHost( 'h3' )
        Host3 = self.addHost( 'h4' )
        Host4 = self.addHost( 'h5' )
        Host5 = self.addHost( 'h6' )
        Host6 = self.addHost( 'h7' )
        Host7 = self.addHost( 'h8' )
        Host8 = self.addHost( 'h9' )
	coreSwitch = self.addSwitch( 's1' )
        disSwitch1 = self.addSwitch( 's2' )
        disSwitch2 = self.addSwitch( 's3' )
        accSwitch1 = self.addSwitch( 's4' )
        accSwitch2 = self.addSwitch( 's5' )
        accSwitch3 = self.addSwitch( 's6' )
        accSwitch4 = self.addSwitch( 's7' )

        # Add links
        self.addLink( edgeServer, coreSwitch)
        self.addLink( coreSwitch, disSwitch1 )
        self.addLink( coreSwitch, disSwitch2 )
        self.addLink( disSwitch1, disSwitch2 )
        self.addLink( disSwitch1, accSwitch1 )
        self.addLink( disSwitch1, accSwitch2 )
        self.addLink( disSwitch2, accSwitch3 )
        self.addLink( disSwitch2, accSwitch4 )
        self.addLink( accSwitch1, Host1 )
        self.addLink( accSwitch1, Host2 )
        self.addLink( accSwitch2, Host3 )
        self.addLink( accSwitch2, Host4 )
        self.addLink( accSwitch3, Host5 )
        self.addLink( accSwitch3, Host6 )
        self.addLink( accSwitch4, Host7 )
        self.addLink( accSwitch4, Host8 )


topos = { 'mytopo': ( lambda: MyTopo() ) }
