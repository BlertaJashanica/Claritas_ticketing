import subprocess
import xml.etree.ElementTree as ET

def perform_nmap_scan(target_network):
    output_file = 'nmap_scan.xml'
    nmap_command = ['nmap', '-sV', '-O', '--osscan-guess', target_network, '-oX', output_file]
    subprocess.run(nmap_command)
    return output_file

def parse_nmap_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    hosts_info = []

    for host in root.findall('host'):
        ip_address = host.find("address[@addrtype='ipv4']").get('addr')
        hostnames = host.find('hostnames')
        hostname = hostnames.find('hostname').get('name') if hostnames is not None else ip_address

        os_element = host.find(".//os/osmatch")
        os_name = os_element.get('name') if os_element is not None else 'Unknown'

        services = []
        for service in host.findall(".//service"):
            service_dict = {
                'name': service.get('name'),
                'port': service.get('portid'),
                'protocol': service.get('protocol')
            }
            services.append(service_dict)

        hosts_info.append({'ip_address': ip_address, 'hostname': hostname, 'os': os_name, 'services': services})

    return hosts_info

def generate_checkmk_config(hosts_info, output_file='checkmk_hosts.mk'):
    with open(output_file, 'w') as file:
        for host in hosts_info:
            file.write(f"all_hosts += ['{host['hostname']}|lan|ip-v4|ip-v4a|wato|/{host['os']}/' + FOLDER_PATH + '/']\n")
            for service in host['services']:
                file.write(f"extra_service_conf['check_command'].append(('check_mk_active-tcp!{service['port']}', [], ['{host['hostname']}']))\n")

if __name__ == '__main__':
    network = '172.16.183.0/24'  # Adjust the network range as per your requirement
    xml_output = perform_nmap_scan(network)
    hosts_data = parse_nmap_xml(xml_output)
    generate_checkmk_config(hosts_data)
