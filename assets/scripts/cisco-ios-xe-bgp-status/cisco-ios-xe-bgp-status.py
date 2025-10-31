#!/usr/bin/env python3
"""
Cisco IOS-XE BGP Neighbor Status Checker

A script for Cisco IOS-XE devices that checks BGP neighbor status by connecting via SSH.
Returns detailed information about BGP neighbors in JSON format for automation systems.

Automation use cases:
- Network health monitoring: Validate BGP sessions in automated monitoring processes
- Change management: Verify BGP sessions after network changes
- Troubleshooting: Quickly identify BGP session issues within automated workflows

Output format:
- JSON: Structured output for automation systems and dashboards

Parameters:
  --host HOST - Target Cisco IOS-XE device hostname or IP
  --username USERNAME - SSH username
  --password PASSWORD - SSH password
  --neighbor NEIGHBOR_IP - [Optional] Specific BGP neighbor to check

Exit codes:
  0 - Success (successfully retrieved BGP neighbor status)
  1 - Error occurred

Usage examples:
  Check all BGP neighbors:
    python cisco-ios-xe-bgp-status.py --host 10.1.1.1 --username admin --password cisco

  Check specific BGP neighbor:
    python cisco-ios-xe-bgp-status.py --host 10.1.1.1 --username admin --password cisco --neighbor 10.2.2.2
"""

import sys
import json
import argparse
import paramiko
import re

def get_bgp_neighbors(host, username, password, specific_neighbor=None):
    """
    Connect to a Cisco IOS-XE device and retrieve BGP neighbor status.
    
    Args:
        host (str): The hostname or IP address of the Cisco IOS-XE device
        username (str): SSH username for the device
        password (str): SSH password for the device
        specific_neighbor (str, optional): Filter results to a specific BGP neighbor
        
    Returns:
        dict: Structured BGP neighbor data with the following format:
              {
                "device": {
                  "hostname": "ROUTER1",
                  "platform": "Cisco IOS-XE"
                },
                "bgp": {
                  "local_as": "65000",
                  "router_id": "10.0.0.1"
                },
                "neighbors": [
                  {
                    "neighbor_ip": "192.168.1.1",
                    "remote_as": "65001",
                    "state": "Established",
                    "uptime": "1d20h",
                    "prefixes_received": 545,
                    "prefixes_sent": 123,
                    "description": "PEER-ROUTER2"
                  },
                  ...
                ],
                "summary": {
                  "total_neighbors": 5,
                  "established_sessions": 4,
                  "down_sessions": 1
                }
              }
    """
    try:
        # Connect to the device
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=host, 
            username=username, 
            password=password, 
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )
        
        # Get device hostname and platform
        stdin, stdout, stderr = ssh_client.exec_command("show version | include Software")
        version_output = stdout.read().decode()
        platform = "Cisco IOS-XE" if "IOS-XE" in version_output else "Cisco IOS"
        
        stdin, stdout, stderr = ssh_client.exec_command("show running-config | include hostname")
        hostname_output = stdout.read().decode().strip()
        hostname = hostname_output.replace("hostname ", "") if "hostname" in hostname_output else host
        
        # Get BGP router information
        stdin, stdout, stderr = ssh_client.exec_command("show ip bgp summary")
        summary_output = stdout.read().decode()
        
        # Extract BGP local AS and router ID
        local_as_match = re.search(r"local AS number (\d+)", summary_output)
        local_as = local_as_match.group(1) if local_as_match else "Unknown"
        
        router_id_match = re.search(r"BGP router identifier (\d+\.\d+\.\d+\.\d+)", summary_output)
        router_id = router_id_match.group(1) if router_id_match else "Unknown"
        
        # Get BGP neighbors information
        if specific_neighbor:
            stdin, stdout, stderr = ssh_client.exec_command(f"show ip bgp neighbors {specific_neighbor}")
        else:
            stdin, stdout, stderr = ssh_client.exec_command("show ip bgp neighbors")
        
        neighbors_output = stdout.read().decode()
        
        # Parse BGP neighbors details
        neighbors = []
        
        # Regular expressions to extract BGP neighbor details
        neighbor_regex = r"BGP neighbor is (\d+\.\d+\.\d+\.\d+),\s+remote AS (\d+)"
        state_regex = r"BGP state = (\w+)"
        uptime_regex = r"Up for (\d+:\d+:\d+|\d+\w+\d+\w+)"
        prefixes_received_regex = r"(\d+) accepted prefixes"
        prefixes_sent_regex = r"(\d+) announced prefixes"
        description_regex = r"Description: (.*)"
        
        # Split output by BGP neighbor sections
        neighbor_sections = re.split(r"BGP neighbor is", neighbors_output)[1:]
        
        # If no neighbor sections found but command succeeded, return empty neighbors list
        if not neighbor_sections and "% No such neighbor" not in neighbors_output:
            # We have a successful connection but no neighbors configured
            pass
        
        for section in neighbor_sections:
            section = "BGP neighbor is" + section
            neighbor_match = re.search(neighbor_regex, section)
            
            if neighbor_match:
                neighbor_ip = neighbor_match.group(1)
                remote_as = neighbor_match.group(2)
                
                state_match = re.search(state_regex, section)
                state = state_match.group(1) if state_match else "Unknown"
                
                uptime_match = re.search(uptime_regex, section)
                uptime = uptime_match.group(1) if uptime_match else "N/A"
                
                prefixes_received_match = re.search(prefixes_received_regex, section)
                prefixes_received = int(prefixes_received_match.group(1)) if prefixes_received_match else 0
                
                prefixes_sent_match = re.search(prefixes_sent_regex, section)
                prefixes_sent = int(prefixes_sent_match.group(1)) if prefixes_sent_match else 0
                
                description_match = re.search(description_regex, section)
                description = description_match.group(1) if description_match else ""
                
                neighbor_info = {
                    "neighbor_ip": neighbor_ip,
                    "remote_as": remote_as,
                    "state": state,
                    "uptime": uptime,
                    "prefixes_received": prefixes_received,
                    "prefixes_sent": prefixes_sent,
                    "description": description
                }
                
                neighbors.append(neighbor_info)
        
        # Calculate BGP session summary
        total_neighbors = len(neighbors)
        established_sessions = sum(1 for n in neighbors if n["state"] == "Established")
        down_sessions = total_neighbors - established_sessions
        
        ssh_client.close()
        
        # Create the full result structure
        result = {
            "device": {
                "hostname": hostname,
                "platform": platform
            },
            "bgp": {
                "local_as": local_as,
                "router_id": router_id
            },
            "neighbors": neighbors,
            "summary": {
                "total_neighbors": total_neighbors,
                "established_sessions": established_sessions,
                "down_sessions": down_sessions
            }
        }
        
        return result
        
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        raise RuntimeError(f"Failed to connect to device: {str(e)}")
    except paramiko.ssh_exception.AuthenticationException as e:
        raise RuntimeError(f"Authentication failed: {str(e)}")
    except Exception as e:
        # If the error is about no BGP session, return an empty neighbors list instead of error
        if "No existing session" in str(e) or "BGP not active" in str(e) or "%BGP" in str(e):
            return {
                "device": {
                    "hostname": hostname if 'hostname' in locals() else host,
                    "platform": platform if 'platform' in locals() else "Cisco IOS-XE"
                },
                "bgp": {
                    "local_as": "Not configured",
                    "router_id": "Not configured" 
                },
                "neighbors": [],
                "summary": {
                    "total_neighbors": 0,
                    "established_sessions": 0,
                    "down_sessions": 0
                },
                "status": "BGP not configured or not active on this device"
            }
        else:
            raise RuntimeError(f"Failed to retrieve BGP neighbor information: {str(e)}")


def main():
    """Main function that handles script execution and output formatting."""
    parser = argparse.ArgumentParser(description='Cisco IOS-XE BGP Neighbor Status Checker')
    parser.add_argument('--host', '-H', required=True, help='Cisco IOS-XE device hostname or IP')
    parser.add_argument('--username', '-u', required=True, help='SSH username')
    parser.add_argument('--password', '-p', required=True, help='SSH password')
    parser.add_argument('--neighbor', '-n', help='Specific BGP neighbor IP to check')
    
    args = parser.parse_args()
    
    try:
        # Try to get BGP neighbor information
        try:
            result = get_bgp_neighbors(args.host, args.username, args.password, args.neighbor)
            print(json.dumps(result, indent=2))
            sys.exit(0)
        except Exception as e:
            # Check if the error is BGP-related but not a connection issue
            if (not isinstance(e, paramiko.ssh_exception.NoValidConnectionsError) and 
                not isinstance(e, paramiko.ssh_exception.AuthenticationException) and
                ("BGP" in str(e) or "No existing session" in str(e))):
                # Create a proper response for when BGP is not configured
                result = {
                    "device": {
                        "hostname": args.host,
                        "platform": "Cisco IOS-XE"
                    },
                    "bgp": {
                        "local_as": "Not configured",
                        "router_id": "Not configured"
                    },
                    "neighbors": [],
                    "summary": {
                        "total_neighbors": 0,
                        "established_sessions": 0,
                        "down_sessions": 0
                    },
                    "status": "BGP not configured or not active on this device"
                }
                print(json.dumps(result, indent=2))
                sys.exit(0)  # This is not an error condition
            else:
                raise  # Re-raise the exception for other errors
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