# Script Requirements

This directory contains specific requirements files for each Python script.

## Installing Requirements

To install the requirements for a specific script, use:

```bash
pip install -r requirements/script-name.txt
```

## Available Requirements Files

- `cisco-ios-xe-bgp-status.txt`: Requirements for checking BGP neighbor status on Cisco IOS-XE devices
- `arista-eos-port-utilization.txt`: Requirements for monitoring port utilization on Arista EOS switches
- `juniper-junos-ospf-status.txt`: Requirements for checking OSPF status on Juniper JUNOS devices
- `dns-domain-checker.txt`: Requirements for checking DNS domain records

## Dependency Notes

Each script has its own requirements file to minimize unnecessary dependencies. This allows for:

- Smaller runtime environments
- Faster installation times
- Fewer dependency conflicts
- Independent versioning of dependencies

When using these scripts with automation platforms like IAG5, you can specify these requirements files to ensure only the necessary dependencies are installed for each script.