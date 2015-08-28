#!/usr/bin/python

#Switch SNMP Interface Test

#TODO
#add ifLastChange ifInDiscards ifInErrors ifOutDiscards ifOutErrors

#Parameters:
verbose = False
SNMP_VERSION = 2
SNMP_COMMUNITY = 0
SNMP_HOST = 0
#IFACE_EXCEPT = [ "Vlan", "Null", ".0", "bme", "vcp", "lsi", "dsc", "lo0", "vlan", "tap", "gre", "ipip", "pime", "pimd", "mtun" ]
IFACE_EXCEPT = [ "WAN Miniport", "Microsoft ISATAP Adapter", ]
ALIAS_EXCEPT = [ "unmonitored", "desktop", "phone" , "iptv", "workstation", "ny7ww7", ]
skip=0
return_code=0
critical_ports=[]

import getopt, sys
import netsnmp

def usage(exit_code):
    print 'Gathers SNMP data from Switch and Alerts if a port that should be up is down'
    print '%s -C <community> -H <hostname>' % sys.argv[0]
    print 'Options'
    print '-C or --community= SNMP Community'
    print '-H or --host=      Host'
    print '-h or --help       Show Help'
    sys.exit(exit_code)

#Parse Arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"C:H:h",["community=","host","help",])
except getopt.GetoptError:
        usage(2)
for opt, arg in opts:
    if opt in ("-h",   "--help"):
        usage(0)
    elif opt in ("-C", "--community"):
        SNMP_COMMUNITY= arg
    elif opt in ("-H", "--host"):
        SNMP_HOST = arg

#require parameters
if not SNMP_COMMUNITY or not SNMP_HOST:
    usage(2)

#print "Querying %s with community %s" % (SNMP_HOST, SNMP_COMMUNITY)

args = {
         "Version": SNMP_VERSION,
         "DestHost": SNMP_HOST,
         "Community": SNMP_COMMUNITY,
         "Timeout": 3000000,
         "Retries": 1,
         }
adminStatuses = { 
    '1' : "up",
    '2' : "down",
    '3' : "testing"
}
operStatuses = { 
    '1' : "up",
    '2' : "down",
    '3' : "testing",
    '4' : "unknown",
    '5' : "dormant",
    '6' : "notPresent",
    '7' : "lowerLayerDown"
}

sess = netsnmp.Session (**args)
INDEX_POS = 0
MIB_ROOT = "ifIndex"
MIB_CURR = MIB_ROOT
RESULTS = {} 
while (MIB_ROOT == MIB_CURR):
    vars = netsnmp.VarList(netsnmp.Varbind(MIB_CURR,INDEX_POS))
    vals = sess.getbulk(0,16,vars)
    if not vals:
        print("UNKNOWN: Could not talk to host %s" %  SNMP_HOST)
        exit(3)
    for i in vars:
        if (i.tag == MIB_CURR):
            KEY = i.iid
            RESULTS[KEY] = i
    INDEX_POS = int(vars[-1].iid)
    MIB_CURR = vars[-1].tag
for idx in RESULTS:
    descr, alias, operStatus, adminStatus = netsnmp.snmpget(
        netsnmp.Varbind("IF-MIB::ifDescr", idx),
        netsnmp.Varbind("IF-MIB::ifAlias", idx),
        netsnmp.Varbind("IF-MIB::ifOperStatus", idx),
        netsnmp.Varbind("IF-MIB::ifAdminStatus", idx),
        **args)
    skip=0 #reset skip or it will skip as soon as it finds it's first exception
    assert(descr is not None)
    if descr == "lo":
        continue
    #Skip Admin Down Interfaces
    if adminStatus != "1": 
        continue
    #Skip Interfaces that are working
    if operStatus == "1":
        continue
    for term in ALIAS_EXCEPT:
        if term in alias:
            skip = 1
    #Skip stupid 3750 switches where we cannot shutdown the stacksub ports
    if 'ny4npintsw1' in SNMP_HOST or 'ny4ncsw1' in SNMP_HOST and 'Stack' in descr:
        skip = 1
    for term in IFACE_EXCEPT:
        if term in descr:
            skip = 1
    if skip == 0:
        critical_ports.append("Interface:%s Alias:%s adminStatus=%s operStatus=%s." % (descr, alias, adminStatuses[adminStatus], operStatuses[operStatus]))
        return_code=2

if return_code==2:
    print('CRITICAL:'),
    for key in critical_ports:
        print (key + ' '),
    exit(return_code)
if return_code==0:
    print('OK:')
    exit(return_code)

exit(return_code)
