# Network Automation Scripts

This directory contains network automation scripts organized in a modular structure. Each script is in its own directory along with its requirements file.

## Directory Structure

```
scripts/
├── arista-eos-port-utilization/
│   ├── arista-eos-port-utilization.py
│   └── requirements.txt
├── cisco-ios-xe-bgp-status/
│   ├── cisco-ios-xe-bgp-status.py
│   └── requirements.txt
├── dns-domain-checker/
│   ├── dns-domain-checker.py
│   └── requirements.txt
├── juniper-junos-ospf-status/
│   ├── juniper-junos-ospf-status.py
│   └── requirements.txt
└── README.md
```

## Running Scripts

Each script can be run directly from its directory:

```bash
cd scripts/cisco-ios-xe-bgp-status
pip install -r requirements.txt
python cisco-ios-xe-bgp-status.py --host 10.1.1.1 --username admin --password cisco
```

## Available Scripts

- **cisco-ios-xe-bgp-status**: Checks BGP neighbor status on Cisco IOS-XE devices
- **arista-eos-port-utilization**: Monitors port utilization on Arista EOS switches
- **juniper-junos-ospf-status**: Checks OSPF status on Juniper JUNOS devices
- **dns-domain-checker**: Validates DNS record existence for a given hostname

## IAG5 Integration

When registering these scripts with IAG5, use the following structure:

```
iagctl create service python-script cisco-ios-xe-bgp-status \
--repository autocon3-content \
--filename cisco-ios-xe-bgp-status.py \
--working-dir scripts/cisco-ios-xe-bgp-status \
--description "Python script that checks BGP neighbor status on Cisco IOS-XE devices" \
--decorator "cisco-ios-xe-bgp-status-decorator"
```

Note the updated `--working-dir` path to reflect the new directory structure.