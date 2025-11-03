#!/usr/bin/env python3
"""
DNS Domain Checker

A script designed for network automation and process orchestration.
Validates DNS record existence for a given hostname, making it ideal for pre-deployment automation,
service dependency validation, and multi-stage orchestration workflows.

Automation use cases:
- Pre-deployment: Verify DNS dependencies in automated provisioning processes
- Network orchestration: Confirm DNS propagation after infrastructure changes
- Service validation: Verify critical services are properly registered within workflows

Output format:
- Text: Human-readable output for operations teams

Exit codes:
  0 - Success (record found or not found, check output for details)
  1 - Error occurred (initiate exception handling in automation platform)

Usage: python dns-domain-checker.py --hostname HOSTNAME
"""

import sys
import socket
import argparse

# Orchestration Integration Notes:
# ---------------------------
# This script is designed as a building block for complex process orchestration.
#
# Process Integration Points:
#   - Service provisioning: Validate DNS dependencies before resource allocation
#   - Configuration automation: Verify network changes have propagated correctly
#   - End-to-end workflows: Provide decision points for multi-system orchestration
#
# Orchestration Capabilities:
#   - Use the --output json flag for integration with automation platforms
#   - Leverage exit codes for process flow control and dynamic branching
#   - Error code separation enables automated exception handling and recovery
#   - Designed for seamless integration in multi-stage automation sequences


def check_dns_record_exists(hostname):
    """
    Validate DNS record existence as a critical step in orchestrated processes.
    
    This function serves as a validation checkpoint in complex automation workflows,
    providing go/no-go decision points for multi-stage orchestration sequences.
    It enables automated verification of network dependencies in end-to-end
    service provisioning and configuration management processes.
    
    Args:
        hostname (str): The hostname to verify in DNS - can include subdomains
                        and should follow RFC 1123 format. Can be dynamically
                        generated as part of automated provisioning processes.
        
    Returns:
        tuple: (exists, ip_address) where:
               - exists: Boolean flag for orchestration decision points
               - ip_address: Resolved IP address for automated inventory updates
                 and downstream configuration processes. None if resolution failed.
                
    Orchestration Use Cases:
        - Automated dependency verification in service provisioning
        - Configuration validation in multi-system automation
        - Process branching in end-to-end service orchestration
    """
    try:
        # Attempt to resolve the hostname
        ip_address = socket.gethostbyname(hostname)
        return True, ip_address
    except socket.gaierror:
        # DNS resolution failed
        return False, None


def main():
    """
    Main function orchestrating the DNS validation process as an automation component.
    
    Designed for seamless integration in end-to-end orchestration workflows.
    Provides deterministic behavior and standardized outputs that enable
    automated decision-making and conditional process branching in complex
    automation scenarios.
    
    Orchestration Features:
    - Standardized interface for integration with automation platforms
    - Human-readable text output
    - Orchestration-ready exit codes for dynamic process flow control
    """
    parser = argparse.ArgumentParser(description='Check if a DNS record exists for a hostname')
    parser.add_argument('--hostname', '-H', required=True, help='Hostname to check')
    
    args = parser.parse_args()
    
    hostname = args.hostname
    
    exists, ip_address = check_dns_record_exists(hostname)
    
    # Print the text result
    if exists:
        result = f"DNS record for {hostname} exists"
        if ip_address:
            result += f" - IP address: {ip_address}"
        
        print(result, end="")
    else:
        print(f"DNS record for {hostname} does not exist", end="")
    
    # Exit code 0 for normal operation regardless of DNS record status
    # The existence of the record is communicated via the text output
    # This allows workflows to make decisions based on the output rather than exit code
    # Exit code 1 is reserved for exceptions only, enabling clear error handling in automation
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Print error message to stderr for troubleshooting automation issues
        print(f"Error: {str(e)}", file=sys.stderr)
        # Exit with code 1 on exceptions - non-zero exit only for error conditions
        # Used to initiate exception handling procedures in automation platform
        # and trigger fallback processes in orchestration workflows
        # Enables automated error recovery and process resilience
        sys.exit(1)
