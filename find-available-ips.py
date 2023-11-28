#!/usr/bin/env python3
import ipaddress
import subprocess

def scan_network(ip_range):
    command = f"nmap -sn {ip_range}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode("utf-8")

def find_available_ips(ip_range, scan_result):
    scanned_ips = set(line.split()[-1] for line in scan_result.splitlines() if "Nmap scan report" in line)
    all_ips = set(str(ip) for ip in ipaddress.IPv4Network(ip_range, strict=False).hosts())
    available_ips = all_ips - scanned_ips
    return available_ips

if __name__ == "__main__":
    network_range = input("Enter the network range (e.g., 10.0.100.0/24): ")
    scan_result = scan_network(network_range)
    available_ips = find_available_ips(network_range, scan_result)

    print("Available IPs:")
    for ip in sorted(available_ips, key=lambda x: ipaddress.IPv4Address(x)):
        print(ip)
