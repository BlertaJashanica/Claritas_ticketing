import os
import json
import requests
import sys

def run_command(command):
    return os.popen(command).read()

def post_to_checkmk(ip, hostname):
    url = 'http://localhost:5000/cmk/check_mk/api/1.0/domain-types/host_config/collections/all?bake_agent=false'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer username password',
        'Content-Type': 'application/json'
    }
    data = {
        'folder': '/script',
        'host_name': hostname,
        'attributes': {
            'ipaddress': ip
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text

def scan_network(network):
    # Initial command to discover hosts in the given network
    initial_scan_output = run_command(f'sudo nmap -sn {network} --min-rate 1000 -T4')
    ip_addresses = []
    for line in initial_scan_output.split('\n'):
        if "Nmap scan report for" in line:
            ip = line.split()[-1].strip('()')
            ip_addresses.append(ip)
    return ip_addresses

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python discovery.py <network1> <network2> ...")
        sys.exit(1)

    networks = sys.argv[1:]
    host_details = {}
    responses = []

    for network in networks:
        ip_addresses = scan_network(network)
        for ip in ip_addresses:
            os_output = run_command(f'sudo nmap -O --osscan-guess -A -v {ip}')
            details = {
                'IP': ip,
                'Hostname': '',
                'OS': []
            }
            hostname = ip  # Default to IP if no hostname is found
            for line in os_output.split('\n'):
                if "Nmap scan report for" in line:
                    hostname = line.split(' ')[4] if '(' in line and not line.endswith(')') else ip
                    details['Hostname'] = hostname.strip('()')
                elif "Running:" in line or "Aggressive OS guesses:" in line:
                    os_info = line.split(":")[1].split(", ")
                    details['OS'] = os_info

            host_details[ip] = details
            # Posting to Checkmk
            status, text = post_to_checkmk(ip, hostname)
            responses.append((ip, status, text))

    # Save the results in a JSON file
    with open('discovery.json', 'w') as json_file:
        json.dump(host_details, json_file, indent=4)

    # Output API responses for review
    for response in responses:
        print(f"IP: {response[0]}, Status: {response[1]}, Response: {response[2]}")

    print("OS discovery, hostname retrieval, and Checkmk updates are complete. Results are saved in discovery.json.")