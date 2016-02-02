from os import getcwd
import snmpy

device = '10.100.184.62'
public = 'public'
private = 'private'

client = snmpy.Snmpy(device, public, private)

client.add_mib_path(getcwd())

# NOTE: In order to use this, download the APC PowerNet-MIB from:
#       ftp://ftp.apc.com/apc/public/software/pnetmib/mib
# and run:
#       build-pysnmp-mib -o PowerNet-MIB.py powernetZZZ.mib
# There appears to be a bug in either the MIB or build-pysnmp-mib whereby
# Unsigned32 is undefined. Despite this being an awful hack, modify the
# generated PowerNet-MIB.py running:
#       sed -i '10 a ( Unsigned32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Unsigned32")' PowerNet-MIB.py
client.load_mibs('PowerNet-MIB')

print client.alive
print "APC Model Number: %s" % \
      client.get('PowerNet-MIB::rPDU2IdentModelNumber.1')
print "Outlet 5 status: %s" % \
      client.get('PowerNet-MIB::rPDU2OutletSwitchedStatusState.5')
print "Outlet 5 on: %s" % \
      client.set('PowerNet-MIB::rPDU2OutletSwitchedControlCommand.5', 1)
print "Outlet 5 command pending: %s" % \
      client.get('PowerNet-MIB::rPDU2OutletSwitchedStatusCommandPending.5')
print "Outlet 5 status: %s" % \
      client.get('PowerNet-MIB::rPDU2OutletSwitchedStatusState.5')
print "Outlet 5 off: %s" % \
      client.set('PowerNet-MIB::rPDU2OutletSwitchedControlCommand.5', 1)
print "Outlet 5 command pending: %s" % \
      client.get('PowerNet-MIB::rPDU2OutletSwitchedStatusCommandPending.5')
print "Outlet 5 status: %s" % \
      client.get('PowerNet-MIB::rPDU2OutletSwitchedStatusState.5')
