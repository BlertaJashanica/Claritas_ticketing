# Dit script is verantwoordelijk voor het scannen van het lokale netwerk voor online hosts. De gevonden
# hosts worden naar de checkmk inventory gepusht in de juiste folders afhankelijk van de inhoud van mappings.txt.
# Vervolgens wordt er ook OS detectie uitgevoerd.

import os
import json
import requests

def run_command(command):
    return os.popen(command).read()

def post_to_checkmk(ip, hostname, os, folder):
    url = 'http://localhost:5000/cmk/check_mk/api/1.0/domain-types/host_config/collections/all?bake_agent=false'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer TOKEN',
        'Content-Type': 'application/json'
    }
    data = {
        'folder': f'/{folder}',
        'host_name': hostname,
        'attributes': {
            'ipaddress': ip,
            'labels': {
                'os': os
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text

def scan_network(network):
    # Initial command to discover hosts in the given network
    initial_scan_output = run_command(f'nmap -sn {network} --min-rate 1000 -T4')
    ip_addresses = []
    for line in initial_scan_output.split('\n'):
        if "Nmap scan report for" in line:
            ip = line.split()[-1].strip('()')
            ip_addresses.append(ip)
    return ip_addresses

def is_port_open(scan_output, port):
    for line in scan_output.splitlines():
        if f"{port}/tcp" in line:
            return "open" in line
    return False

def port_scan(target, port):
    initial_scan_output = run_command(f'nmap -p {port} {target}')
    return is_port_open(initial_scan_output, port)

def load_mappings(filename='/home/clari-group5/scripts/mappings.txt'):
    with open(filename, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    # Load mappings from file
    mappings = load_mappings()
    host_details = {}
    responses = []

    for folder, network in mappings.items():
        ip_addresses = scan_network(network)
        for ip in ip_addresses:
            os_output = run_command(f'sudo nmap -O --osscan-guess -A -v {ip}')
            details = {
                'IP': ip,
                'Hostname': '',
                'OS': []
            }
            hostname = ip  # Default to IP if no hostname is found
            os_info = []

            for line in os_output.split('\n'):
                if "Nmap scan report for" in line:
                    hostname = line.split(' ')[4].strip('()') if '(' in line and not line.endswith(')') else ip
                    details['Hostname'] = hostname
                elif "Running:" in line:
                    os_info.extend(line.split(":")[1].strip().split(", "))
                elif "OS details:" in line:
                    os_info.extend(line.split(":")[1].strip().split(", "))
                elif "Aggressive OS guesses:" in line:
                    os_info.extend(line.split(":")[1].strip().split(", "))

            os_info = os_info[0].split()[0]
            details['OS'] = os_info
            host_details[ip] = details

            # Posting to Checkmk
            status, text = post_to_checkmk(ip, hostname, os_info, folder)
            responses.append((ip, status, text))

    # Save the results in a JSON file
    with open('discovery.json', 'w') as json_file, json_file:
        json.dump(host_details, json_file, indent=4)

    # Output API responses for review
    for response in responses:
        print(f"IP: {response[0]}, Status: {response[1]}, Response: {response[2]}")

    print("OS discovery, hostname retrieval, and Checkmk updates are complete. Results are saved in discovery.json.")
