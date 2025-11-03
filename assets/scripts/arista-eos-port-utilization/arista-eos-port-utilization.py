#!/usr/bin/env python3
"""
Arista EOS Switch Port Utilization Analyzer

A script specifically designed for Arista EOS switches that monitors port utilization.
Connects to switches via eAPI and provides detailed port statistics in JSON format,
making it ideal for capacity planning, traffic analysis, and monitoring automation.

This version has additional error handling for better compatibility with different EOS versions.

Output format:
- JSON: Structured output for automation systems and dashboards

Parameters:
  --host HOST - Target Arista EOS switch hostname or IP
  --username USERNAME - eAPI username
  --password PASSWORD - eAPI password
  --transport {http,https} - eAPI transport protocol (default: https)
  --port PORT - eAPI port (default: 443)
  --threshold THRESHOLD - Utilization threshold % to highlight (default: 70)
  --debug - Enable debug output

Exit codes:
  0 - Success
  1 - Error occurred

Usage examples:
  Basic usage:
    python arista-eos-port-utilization.py --host 10.1.1.1 --username admin --password arista

  With HTTP instead of HTTPS:
    python arista-eos-port-utilization.py --host 10.1.1.1 --username admin --password arista --transport http --port 80
"""

import sys
import json
import argparse
import datetime
import ssl
import pyeapi

# Disable SSL certification verification for compatibility with self-signed certificates
ssl._create_default_https_context = ssl._create_unverified_context

def get_port_utilization(connection, threshold=70, debug=False):
    """
    Retrieve port statistics and calculate utilization for Arista EOS switches.
    
    Args:
        connection: pyeapi connection object
        threshold (int): Utilization percentage threshold to highlight (default: 70)
        debug (bool): Enable debug output
        
    Returns:
        dict: Structured port utilization data
    """
    try:
        # Get device information with more robust error handling
        if debug:
            print("DEBUG: Fetching device information...", file=sys.stderr)

        show_version = connection.execute("show version")
        if debug:
            print(f"DEBUG: show version result: {json.dumps(show_version)}", file=sys.stderr)
            
        version_data = show_version["result"][0]
        
        # Set default values for device info
        hostname = "Unknown"
        model = "Unknown"
        serial_number = "Unknown"
        version = "Unknown"
        
        # Extract data with robust error handling
        try:
            hostname = version_data.get("hostname", "Unknown")
        except (KeyError, TypeError):
            pass
            
        try:
            model = version_data.get("modelName", "Unknown")
        except (KeyError, TypeError):
            pass
            
        try:
            serial_number = version_data.get("serialNumber", "Unknown")
        except (KeyError, TypeError):
            pass
            
        try:
            version = version_data.get("version", "Unknown")
        except (KeyError, TypeError):
            pass
            
        # Use the host provided if hostname is not available
        if hostname == "Unknown":
            hostname = connection.transport.host
        
        device_info = {
            "hostname": hostname,
            "platform": "Arista EOS",
            "model": model,
            "serial_number": serial_number,
            "version": version
        }
        
        if debug:
            print(f"DEBUG: Device info: {json.dumps(device_info)}", file=sys.stderr)
            
        # Get interface descriptions
        if debug:
            print("DEBUG: Fetching interface descriptions...", file=sys.stderr)
            
        show_interfaces_description = connection.execute("show interfaces description")
        interface_descriptions = {}
        
        try:
            interface_descriptions = show_interfaces_description["result"][0].get("interfaceDescriptions", {})
        except (KeyError, IndexError):
            if debug:
                print("DEBUG: Error parsing interface descriptions", file=sys.stderr)
        
        # Get interface status
        if debug:
            print("DEBUG: Fetching interface status...", file=sys.stderr)
            
        show_interfaces_status = connection.execute("show interfaces status")
        interface_status = {}
        
        try:
            interface_status = show_interfaces_status["result"][0].get("interfaceStatuses", {})
        except (KeyError, IndexError):
            if debug:
                print("DEBUG: Error parsing interface status", file=sys.stderr)
        
        # Get interface counters
        if debug:
            print("DEBUG: Fetching interface counters...", file=sys.stderr)
            
        show_interfaces_counters = connection.execute("show interfaces counters")
        interface_counters = {}
        
        try:
            interface_counters = show_interfaces_counters["result"][0].get("interfaces", {})
        except (KeyError, IndexError):
            if debug:
                print("DEBUG: Error parsing interface counters", file=sys.stderr)
        
        # Get interface rates
        if debug:
            print("DEBUG: Fetching interface rates...", file=sys.stderr)
            
        show_interfaces_rates = connection.execute("show interfaces counters rates")
        interface_rates = {}
        
        try:
            interface_rates = show_interfaces_rates["result"][0].get("interfaces", {})
        except (KeyError, IndexError):
            if debug:
                print("DEBUG: Error parsing interface rates", file=sys.stderr)
        
        # Get interface errors
        if debug:
            print("DEBUG: Fetching interface errors...", file=sys.stderr)
            
        show_interfaces_errors = connection.execute("show interfaces counters errors")
        interface_errors = {}
        
        try:
            interface_errors = show_interfaces_errors["result"][0].get("interfaceCounters", {})
        except (KeyError, IndexError):
            if debug:
                print("DEBUG: Error parsing interface errors", file=sys.stderr)
        
        # Collect all Ethernet interfaces
        interfaces = []
        high_utilization_count = 0
        error_interfaces_count = 0
        active_interfaces_count = 0
        
        for interface_name, status in interface_status.items():
            try:
                # Only process Ethernet interfaces
                if not interface_name.startswith("Ethernet"):
                    continue
                    
                # Get interface description
                description = ""
                try:
                    description = interface_descriptions.get(interface_name, {}).get("description", "")
                except (TypeError, KeyError):
                    pass
                
                # Get interface bandwidth
                bandwidth_mbps = 0
                try:
                    bandwidth_mbps = int(status.get("bandwidth", 0)) / 1000000 if "bandwidth" in status else 0
                except (TypeError, KeyError, ValueError):
                    pass
                
                # Get interface status
                oper_status = "unknown"
                try:
                    oper_status = status.get("linkStatus", "unknown")
                except (TypeError, KeyError):
                    pass
                
                # Only count active interfaces
                if oper_status == "up":
                    active_interfaces_count += 1
                
                # Get interface rates
                input_rate_mbps = 0
                output_rate_mbps = 0
                
                try:
                    input_rate_mbps = float(interface_rates.get(interface_name, {}).get("inRate", 0)) if interface_name in interface_rates else 0
                except (TypeError, KeyError, ValueError):
                    pass
                
                try:
                    output_rate_mbps = float(interface_rates.get(interface_name, {}).get("outRate", 0)) if interface_name in interface_rates else 0
                except (TypeError, KeyError, ValueError):
                    pass
                
                # Calculate utilization percentage
                input_utilization = (input_rate_mbps / bandwidth_mbps * 100) if bandwidth_mbps > 0 else 0
                output_utilization = (output_rate_mbps / bandwidth_mbps * 100) if bandwidth_mbps > 0 else 0
                
                # Check if utilization exceeds threshold
                high_utilization = input_utilization > threshold or output_utilization > threshold
                if high_utilization:
                    high_utilization_count += 1
                
                # Get error counters
                input_errors = 0
                output_errors = 0
                
                try:
                    input_errors = int(interface_errors.get(interface_name, {}).get("inErrors", 0)) if interface_name in interface_errors else 0
                except (TypeError, KeyError, ValueError):
                    pass
                
                try:
                    output_errors = int(interface_errors.get(interface_name, {}).get("outErrors", 0)) if interface_name in interface_errors else 0
                except (TypeError, KeyError, ValueError):
                    pass
                
                if input_errors > 0 or output_errors > 0:
                    error_interfaces_count += 1
                
                # Collect interface information
                interface_info = {
                    "name": interface_name,
                    "description": description,
                    "status": oper_status,
                    "bandwidth_mbps": bandwidth_mbps,
                    "input_rate_mbps": round(input_rate_mbps, 2),
                    "output_rate_mbps": round(output_rate_mbps, 2),
                    "input_utilization": round(input_utilization, 2),
                    "output_utilization": round(output_utilization, 2),
                    "input_errors": input_errors,
                    "output_errors": output_errors,
                    "high_utilization": high_utilization
                }
                
                interfaces.append(interface_info)
            except Exception as e:
                if debug:
                    print(f"DEBUG: Error processing interface {interface_name}: {str(e)}", file=sys.stderr)
        
        # Sort interfaces by utilization (highest first)
        interfaces.sort(key=lambda x: max(x["input_utilization"], x["output_utilization"]), reverse=True)
        
        # Create summary
        summary = {
            "total_interfaces": len(interfaces),
            "active_interfaces": active_interfaces_count,
            "high_utilization_interfaces": high_utilization_count,
            "error_interfaces": error_interfaces_count
        }
        
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        # Create the result structure
        result = {
            "device": device_info,
            "timestamp": timestamp,
            "interfaces": interfaces,
            "summary": summary
        }
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve port utilization data: {str(e)}")


def main():
    """Main function that handles script execution and output formatting."""
    parser = argparse.ArgumentParser(description='Arista EOS Switch Port Utilization Analyzer')
    parser.add_argument('--host', '-H', required=True, help='Arista EOS switch hostname or IP')
    parser.add_argument('--username', '-u', required=True, help='eAPI username')
    parser.add_argument('--password', '-p', required=True, help='eAPI password')
    parser.add_argument('--transport', '-t', default='https', choices=['http', 'https'], help='eAPI transport protocol (default: https)')
    parser.add_argument('--port', '-P', type=int, default=443, help='eAPI port (default: 443)')
    parser.add_argument('--threshold', '-T', type=int, default=70, help='Utilization threshold %% to highlight (default: 70)')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    try:
        if args.debug:
            print(f"DEBUG: Connecting to {args.host} via {args.transport} on port {args.port}...", file=sys.stderr)
            
        # Create connection to the Arista switch
        node = pyeapi.connect(
            transport=args.transport,
            host=args.host,
            username=args.username,
            password=args.password,
            port=args.port
        )
        
        if args.debug:
            print("DEBUG: Connection established, retrieving port utilization data...", file=sys.stderr)
            
        # Get port utilization data
        result = get_port_utilization(node, args.threshold, args.debug)
        
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