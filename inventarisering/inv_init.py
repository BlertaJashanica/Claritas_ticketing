# Script verantwoordelijk voor het initialiseren van de checkmk inventory. Het neemt input in formaat:
#
# '<folder1>:<netwerk1>,<folder2>:<netwerk2>,...' (vb: 'management:10.1.1.0/24,databases:10.1.2.0/24')
#
# De folders worden vervolgens aangemaakt en resultaten worden weggeschreven naar ./mappings.txt.

import sys
import requests
import json

def save_mappings(mappings, filename='mappings.txt'):
    with open(filename, 'w') as file:
        json.dump(mappings, file)

def create_folder(folder, headers, api_url):
    url = f'{api_url}/domain-types/folder_config/collections/all'
    data = {
        'parent': '/',
        'title': folder
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Successfully created folder: {folder}")
    else:
        print(f"Failed to create folder: {folder}. Status Code: {response.status_code}, Response: {response.text}")

def main(input_string):
    api_url = 'http://localhost:5000/cmk/check_mk/api/1.0'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer TOKEN',  # Replace with your token
        'Content-Type': 'application/json'
    }

    # Parse the input string
    folder_network_pairs = input_string.split(',')
    mappings = {}
    for pair in folder_network_pairs:
        folder, network = pair.split(':')
        folder = folder.strip()
        network = network.strip()
        mappings[folder] = network
        create_folder(folder, headers, api_url)
    
    # Save mappings to a local file
    save_mappings(mappings)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inv_init.py \"folder1:network1,folder2:network2,...\"")
    else:
        input_string = sys.argv[1]
        main(input_string)
