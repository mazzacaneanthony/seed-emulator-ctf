#!/usr/bin/env python3
# encoding: utf-8

from seedemu.layers import Base, Routing, Ebgp
from seedemu.services import WebService
from seedemu.compiler import Docker
from seedemu.core import Emulator, Binding, Filter


# Initialize the emulator and layers
emu     = Emulator()
base    = Base()
routing = Routing()
ebgp    = Ebgp()
web     = WebService()

###############################################################################
# Create an Internet Exchange
base.createInternetExchange(100)

###############################################################################
# Create and set up AS-150

# Create an autonomous system 
as150 = base.createAutonomousSystem(150)

# Create a network 
as150.createNetwork('net0')

# Create a router and connect it to two networks
as150.createRouter('router0').joinNetwork('net0').joinNetwork('ix100').addSoftware('nmap')

# Create a host called web and connect it to a network
as150.createHost('ctf-target').joinNetwork('net0').importFile('/home/seed/seed-emulator-ctf/vuln.tar.gz', '/vuln.tar.gz').appendStartCommand('tar -xzf /vuln.tar.gz').appendStartCommand('/vuln/vuln.sh', fork=True)

# Create a web service on virtual node, give it a name
# This will install the web service on this virtual node
web.install('ctf-target')

# Bind the virtual node to a physical node 
emu.addBinding(Binding('ctf-target', filter = Filter(nodeName = 'ctf-target', asn = 150)))


###############################################################################
# Create and set up AS-151
# It is similar to what is done to AS-150

as151 = base.createAutonomousSystem(151)
as151.createNetwork('net0')
as151.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')

as151.createHost('web').joinNetwork('net0')
web.install('web151')
emu.addBinding(Binding('web151', filter = Filter(nodeName = 'web', asn = 151)))

###############################################################################
# Create and set up AS-152
# It is similar to what is done to AS-150

as152 = base.createAutonomousSystem(152)
as152.createNetwork('net0')
as152.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')

as152.createHost('web').joinNetwork('net0')
web.install('web152')
emu.addBinding(Binding('web152', filter = Filter(nodeName = 'web', asn = 152)))


# Extra ASNs
# almazzac

as153 = base.createAutonomousSystem(153)
as153.createNetwork('net0')
as153.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')

as153.createHost('web').joinNetwork('net0')
web.install('web153')
emu.addBinding(Binding('web153', filter = Filter(nodeName = 'web', asn = 153)))


as154 = base.createAutonomousSystem(154)
as154.createNetwork('net0')
as154.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')

as154.createHost('web').joinNetwork('net0')
web.install('web154')
emu.addBinding(Binding('web154', filter = Filter(nodeName = 'web', asn = 154)))

###############################################################################
# Peering these ASes at Internet Exchange IX-100

ebgp.addRsPeer(100, 150)
ebgp.addRsPeer(100, 151)
ebgp.addRsPeer(100, 152)
ebgp.addRsPeer(100, 153)
ebgp.addRsPeer(100, 154)

###############################################################################
# Rendering 

emu.addLayer(base)
emu.addLayer(routing)
emu.addLayer(ebgp)
emu.addLayer(web)

emu.render()

###############################################################################
# Compilation

docker = Docker(internetMapEnabled=True)
emu.compile(docker, './output', override=True)

