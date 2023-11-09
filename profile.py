"""4 node topology for a load balancer test:  src - lb - (sink1, sink2)

Instructions:
Use ipvs on lb, then curl from src."""

BLOCKSTORE_SIZE=30

## COPIED FROM small-lan

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


# Add a raw PC to the request and give it an interface.
src = request.RawPC("src")
#src.hardware_type = "d710"
src.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
src_iface0 = src.addInterface()
src_iface0.addAddress(pg.IPv4Address("10.1.1.1", "255.255.255.0"))
# Add extra storage space
bs = node.Blockstore("src" + "-bs", "/mydata")
bs.size = str(BLOCKSTORE_SIZE) + "GB"
bs.placement = "any"



# Add a raw PC to the request and give it an interface.
lb = request.RawPC("lb")
lb.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
lb_iface0 = lb.addInterface()
lb_iface0.addAddress(pg.IPv4Address("10.1.1.2", "255.255.255.0"))
lb_iface1 = lb.addInterface()
lb_iface1.addAddress(pg.IPv4Address("192.168.1.1", "255.255.255.0"))
bs = node.Blockstore("lb" + "-bs", "/mydata")
bs.size = str(BLOCKSTORE_SIZE) + "GB"
bs.placement = "any"

# Add another raw PC to the request and give it an interface.
sink1 = request.RawPC("sink1")
sink1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
sink1_iface0 = sink1.addInterface()
sink1_iface0.addAddress(pg.IPv4Address("192.168.1.2", "255.255.255.0"))
bs = node.Blockstore("sink1" + "-bs", "/mydata")
bs.size = str(BLOCKSTORE_SIZE) + "GB"
bs.placement = "any"

# Add another raw PC to the request and give it an interface.
sink2 = request.RawPC("sink2")
sink2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
sink2_iface0 = sink2.addInterface()
sink2_iface0.addAddress(pg.IPv4Address("192.168.1.3", "255.255.255.0"))
bs = node.Blockstore("sink2" + "-bs", "/mydata")
bs.size = str(BLOCKSTORE_SIZE) + "GB"
bs.placement = "any"

# Add a link to the request and then add the interfaces to the link
link1 = request.Link("link-src-lb")
link1.addInterface(src_iface0)
link1.addInterface(lb_iface0)
#link1.bandwidth = 1000000


link = request.LAN("lb-sinks")
link.addInterface(lb_iface1)
link.addInterface(sink1_iface0)
link.addInterface(sink2_iface0)



# Specify duplex parameters for each of the nodes in the link (or lan).
# BW is in Kbps
#link.bandwidth = 1000000
# Latency is in milliseconds
#link.latency = 10
# Packet loss is a number 0.0 <= loss <= 1.0
#link.plr = 0.05

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
