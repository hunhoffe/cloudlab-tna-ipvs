"""4 node topology for a load balancer test:  src - lb - (sink1, sink2)

Instructions:
Use ipvs on lb, then curl from src."""

BLOCKSTORE_SIZE=100
TNA_IMAGE="urn:publicid:IDN+emulab.net+image+CUDevOpsFall2018:tna-ipvs:0"
BASE_IMAGE="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"


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
                   "",
                   longDescription="A specific hardware type to use for all nodes. If not selected, the resource mapper will choose for you.")
# Optional link speed, normally the resource mapper will choose for you based on node availability
pc.defineParameter("linkSpeed",
                   "Link Speed",
                   portal.ParameterType.INTEGER,
                   0,
                   [(0,"Any"),(25000000,"25Gb/s")], #[(0,"Any"),(100000,"100Mb/s"),(1000000,"1Gb/s"),(10000000,"10Gb/s"),(25000000,"25Gb/s"),(100000000,"100Gb/s")],
                   longDescription="A specific link speed to use for your lan. Make sure you choose a node type that supports it, or let the resource mapper find one.")
params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


# Add a raw PC to the request and give it an interface.
src = request.RawPC("src")

if params.nodeType != "":
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
if params.nodeType != "":
  lb.hardware_type = params.nodeType
lb_iface0 = lb.addInterface()
lb_iface0.addAddress(pg.IPv4Address("10.1.1.2", "255.255.255.0"))
lb_iface1 = lb.addInterface()
lb_iface1.addAddress(pg.IPv4Address("192.168.1.1", "255.255.255.0"))
bs = lb.Blockstore("lb" + "-bs", "/mydata")
bs.size = str(BLOCKSTORE_SIZE) + "GB"
bs.placement = "any"

# Add another raw PC to the request and give it an interface.
sink1 = request.RawPC("sink1")
sink1.disk_image = BASE_IMAGE
if params.nodeType != "":
  sink1.hardware_type = params.nodeType
sink1_iface0 = sink1.addInterface()
sink1_iface0.addAddress(pg.IPv4Address("192.168.1.2", "255.255.255.0"))
#bs = sink1.Blockstore("sink1" + "-bs", "/mydata")
#bs.size = str(BLOCKSTORE_SIZE) + "GB"
#bs.placement = "any"

# Add another raw PC to the request and give it an interface.
sink2 = request.RawPC("sink2")
sink2.disk_image = BASE_IMAGE
if params.nodeType != "":
  sink2.hardware_type = params.nodeType
sink2_iface0 = sink2.addInterface()
sink2_iface0.addAddress(pg.IPv4Address("192.168.1.3", "255.255.255.0"))
#bs = sink2.Blockstore("sink2" + "-bs", "/mydata")
#bs.size = str(BLOCKSTORE_SIZE) + "GB"
#bs.placement = "any"

# Add a link to the request and then add the interfaces to the link
link1 = request.Link("link-src-lb")
link1.addInterface(src_iface0)
link1.addInterface(lb_iface0)
link1.bandwidth = params.linkSpeed


link2 = request.LAN("lb-sinks")
link2.addInterface(lb_iface1)
link2.addInterface(sink1_iface0)
link2.addInterface(sink2_iface0)
link2.bandwidth = params.linkSpeed

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
