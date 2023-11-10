"""4 node topology for a load balancer test:  src - lb - (sink1, sink2)

Instructions:
Use ipvs on lb, then curl from src."""

BLOCKSTORE_SIZE=100
TNA_IMAGE="urn:publicid:IDN+emulab.net+image+CUDevOpsFall2018:tna-ipvs"
BASE_IMAGE="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"
# (10000000,"10Gb/s"),(25000000,"25Gb/s"),(100000000,"100Gb/s")
BANDWIDTH=25000000


## COPIED FROM small-lan

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()
pc.defineParameter("nodeType", 
                   "Node Hardware Type",
                   portal.ParameterType.NODETYPE, 
                   "r6525",
                   longDescription="A specific hardware type to use for all nodes. This profile has been tested with d430 nodes")
params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


# Add a raw PC to the request and give it an interface.
src = request.RawPC("src")
src.hardware_type = params.nodeType
src.disk_image = BASE_IMAGE
src_iface0 = src.addInterface()
src_iface0.addAddress(pg.IPv4Address("10.1.1.1", "255.255.255.0"))
# Add extra storage space
#bs = src.Blockstore("src" + "-bs", "/mydata")
#bs.size = str(BLOCKSTORE_SIZE) + "GB"
#bs.placement = "any"



# Add a raw PC to the request and give it an interface.
lb = request.RawPC("lb")
lb.disk_image = TNA_IMAGE
lb.hardware_type = params.nodeType
lb_iface0 = lb.addInterface()
lb_iface0.addAddress(pg.IPv4Address("10.1.1.2", "255.255.255.0"))
bs = lb.Blockstore("lb" + "-bs", "/mydata")
bs.size = str(BLOCKSTORE_SIZE) + "GB"
bs.placement = "any"

# Add another raw PC to the request and give it an interface.
sink1 = request.RawPC("sink1")
sink1.disk_image = BASE_IMAGE
sink1.hardware_type = params.nodeType
sink1_iface0 = sink1.addInterface()
sink1_iface0.addAddress(pg.IPv4Address("10.1.1.3", "255.255.255.0"))
#bs = sink1.Blockstore("sink1" + "-bs", "/mydata")
#bs.size = str(BLOCKSTORE_SIZE) + "GB"
#bs.placement = "any"

# Add another raw PC to the request and give it an interface.
sink2 = request.RawPC("sink2")
sink2.disk_image = BASE_IMAGE
sink2.hardware_type = params.nodeType
sink2_iface0 = sink2.addInterface()
sink2_iface0.addAddress(pg.IPv4Address("10.1.1.4", "255.255.255.0"))
#bs = sink2.Blockstore("sink2" + "-bs", "/mydata")
#bs.size = str(BLOCKSTORE_SIZE) + "GB"
#bs.placement = "any"

# Add a link to the request and then add the interfaces to the link
link = request.LAN()
link.addInterface(sink1_iface0)
link.addInterface(sink2_iface0)
link.addInterface(src_iface0)
link.addInterface(lb_iface0)
link.bandwidth = BANDWIDTH


# Specify duplex parameters for each of the nodes in the link (or lan).
# BW is in Kbps
#link.bandwidth = 1000000
# Latency is in milliseconds
#link.latency = 10
# Packet loss is a number 0.0 <= loss <= 1.0
#link.plr = 0.05

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
