# check_snmp_interface_status
Check if an interface is configure to be up but is not operational



Gathers SNMP data from Switch and Alerts if a port that should be up is down

./check_snmp_interfaces_status.py -C <community> -H <hostname>

Options

-C or --community= SNMP Community

-H or --host=      Host

-h or --help       Show Help




### This check is very usefull when you need to monitor network devices from Nagios or Icinga at port level.
You can ignore certain types of interfaces or based on name or description.

Example run:

./check_snmp_interfaces_status.py -C dcro -H ny7npswcore1

CRITICAL: Interface:GigabitEthernet3/0/39 Alias:server tw1astbp1 adminStatus=up operStatus=down.  Interface:GigabitEthernet4/0/19 Alias:userxxx workstation adminStatus=up operStatus=down.  Interface:GigabitEthernet5/0/28 Alias:userxxx workstation adminStatus=up operStatus=down.  Interface:GigabitEthernet2/0/34 Alias:unknown unmonitored adminStatus=up operStatus=down.  
