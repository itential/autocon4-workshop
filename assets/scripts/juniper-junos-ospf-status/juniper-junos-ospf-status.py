#!/usr/bin/env python3
"""
Juniper JUNOS OSPF Neighbor Status Checker

A script specifically designed for Juniper JUNOS devices that monitors OSPF neighbor status.
Connects to devices via NETCONF and provides detailed OSPF neighbor information in JSON format,
making it ideal for network monitoring, troubleshooting, and automation workflows.

Automation use cases:
- Network health monitoring: Validate OSPF adjacencies in automated monitoring
- Configuration validation: Verify OSPF relationships after network changes
- Troubleshooting: Quickly identify OSPF neighbor issues
- Orchestration: Feed OSPF data into network automation pipelines

Output format:
- JSON: Structured output for automation systems

Parameters:
  --host HOST - Target Juniper JUNOS device hostname or IP
  --username USERNAME - NETCONF username
  --password PASSWORD - NETCONF password
  --port PORT - NETCONF port (default: 830)
  --instance INSTANCE - OSPF routing-instance (default: master)
  --area AREA - Specific OSPF area to check

Exit codes:
  0 - Success
  1 - Error occurred

Usage examples:
  Basic usage:
    python juniper-junos-ospf-status.py --host 10.1.1.1 --username admin --password juniper

  Check specific OSPF area:
    python juniper-junos-ospf-status.py --host 10.1.1.1 --username admin --password juniper --area 0.0.0.0
"""

import sys
import json
import argparse
import datetime
from jnpr.junos import Device
from lxml import etree

def get_ospf_neighbors(host, username, password, port=830, instance="master", area=None):
    """
    Connect to a Juniper JUNOS device and retrieve OSPF neighbor status.
    
    Args:
        host (str): Hostname or IP address of the Juniper device
        username (str): NETCONF username
        password (str): NETCONF password
        port (int): NETCONF port (default: 830)
        instance (str): Routing instance name (default: master)
        area (str): OSPF area ID to filter by (optional)
        
    Returns:
        dict: Structured OSPF neighbor data with the following format:
              {
                "device": {
                  "hostname": "ROUTER1",
                  "platform": "Juniper JUNOS",
                  "model": "MX480",
                  "version": "20.4R3"
                },
                "timestamp": "2025-05-07T10:15:30",
                "ospf_instance": "master",
                "neighbors": [
                  {
                    "neighbor_id": "10.0.0.1",
                    "neighbor_address": "192.168.1.1",
                    "interface": "ge-0/0/1.0",
                    "state": "Full",
                    "area": "0.0.0.0",
                    "adjacency_time": "1d 20:15:22",
                    "dead_time": "00:00:33"
                  },
                  ...
                ],
                "summary": {
                  "total_neighbors": 5,
                  "full_state_neighbors": 4,
                  "non_full_state_neighbors": 1,
                  "areas": ["0.0.0.0", "0.0.0.1"]
                }
              }
    """
    try:
        # Connect to the Juniper device
        dev = Device(host=host, user=username, passwd=password, port=port)
        dev.open()
        
        # Get device information
        device_info = {
            "hostname": dev.facts["hostname"],
            "platform": "Juniper JUNOS",
            "model": dev.facts["model"],
            "version": dev.facts["version"]
        }
        
        # Construct OSPF RPC command
        if area:
            rpc = dev.rpc.get_ospf_neighbor_information(instance=instance, area=area, extensive=True)
        else:
            rpc = dev.rpc.get_ospf_neighbor_information(instance=instance, extensive=True)
        
        # Parse OSPF neighbor information
        neighbors = []
        areas = set()
        full_state_count = 0
        non_full_state_count = 0
        
        # Process neighbor entries
        for nbr in rpc.findall(".//ospf-neighbor"):
            neighbor_id = nbr.findtext("neighbor-id")
            neighbor_address = nbr.findtext("neighbor-address")
            interface = nbr.findtext("interface-name")
            state = nbr.findtext("ospf-neighbor-state")
            ospf_area = nbr.findtext("ospf-area")
            adjacency_time = nbr.findtext("neighbor-adjacency-time")
            dead_time = nbr.findtext("ospf-neighbor-dead-time")
            
            # Update counters
            areas.add(ospf_area)
            if state == "Full":
                full_state_count += 1
            else:
                non_full_state_count += 1
            
            # Create neighbor entry
            neighbor_info = {
                "neighbor_id": neighbor_id,
                "neighbor_address": neighbor_address,
                "interface": interface,
                "state": state,
                "area": ospf_area,
                "adjacency_time": adjacency_time,
                "dead_time": dead_time
            }
            
            neighbors.append(neighbor_info)
        
        # Create summary
        summary = {
            "total_neighbors": len(neighbors),
            "full_state_neighbors": full_state_count,
            "non_full_state_neighbors": non_full_state_count,
            "areas": list(areas)
        }
        
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        # Close the connection
        dev.close()
        
        # Create the result structure
        result = {
            "device": device_info,
            "timestamp": timestamp,
            "ospf_instance": instance,
            "neighbors": neighbors,
            "summary": summary
        }
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve OSPF neighbor information: {str(e)}")


def main():
    """Main function that handles script execution and output formatting."""
    parser = argparse.ArgumentParser(description='Juniper JUNOS OSPF Neighbor Status Checker')
    parser.add_argument('--host', '-H', required=True, help='Juniper JUNOS device hostname or IP')
    parser.add_argument('--username', '-u', required=True, help='NETCONF username')
    parser.add_argument('--password', '-p', required=True, help='NETCONF password')
    parser.add_argument('--port', '-P', type=int, default=830, help='NETCONF port (default: 830)')
    parser.add_argument('--instance', '-i', default='master', help='OSPF routing-instance (default: master)')
    parser.add_argument('--area', '-a', help='Specific OSPF area to check')
    
    args = parser.parse_args()
    
    try:
        # Get OSPF neighbor data
        result = get_ospf_neighbors(
            args.host, 
            args.username, 
            args.password,
            args.port,
            args.instance,
            args.area
        )
        
        # Always output as JSON for automation consumption
        print(json.dumps(result, indent=2))
        
        # Exit code 0 for successful operation
        sys.exit(0)
        
    except Exception as e:
        # Print error message to stderr
        print(f"Error: {str(e)}", file=sys.stderr)
        
        # Output JSON error for automation
        error_json = {
            "error": str(e),
            "success": False
        }
        print(json.dumps(error_json))
        
        # Exit with code 1 on exceptions
        sys.exit(1)


if __name__ == "__main__":
    main()