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
