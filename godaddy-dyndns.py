#!/usr/local/bin/python3

# MIT License
#
# Copyright (c) 2019-2023 Leon Latsch

from configparser import ConfigParser
import requests
import os
import time

# Global Config
config_file = os.path.dirname(__file__) + "/godaddy-dyndns.conf"
if not os.path.isfile(config_file):
    config_file = os.path.dirname(__file__) + "/config/godaddy-dyndns.conf"

cfg = ConfigParser()
cfg.read(config_file)

if not cfg.has_option("godaddy", "key") or not cfg.has_option("godaddy", "secret") or not cfg.has_option("godaddy", "domain") or not cfg.has_option("godaddy", "hosts"):
    print("[!] Config incomplete")
    exit()

key = cfg.get("godaddy", "key")
secret = cfg.get("godaddy", "secret")
domain = cfg.get("godaddy", "domain")
hosts = cfg.get("godaddy", "hosts").split(",")

watchmode = cfg.get("watchmode", "enabled").lower() in "true"
watchmode_interval = int(cfg.get("watchmode", "interval"))

base_url = "https://api.godaddy.com"
endpoint_records = f"/v1/domains/{domain}/records/"
endpoint_a_records = f"/v1/domains/{domain}/records/A/"

# Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

LAST_IP = os.path.dirname(__file__) + "/.last-ip"

def safe_new_ip(ip):
    f = open(LAST_IP, "w")
    f.write(ip)
    f.close()
    print(f"[*] Cached new ip {ip}")

def get_last_ip():
    try:
        f = open(LAST_IP)
        ip = f.read()
        f.close()
        return ip
    except FileNotFoundError:
        return None

def get_ip():
    r = requests.get("https://api.ipify.org/?format=raw")
    if r.status_code != 200: # Fallback
        r = requests.get("http://ip.42.pl/raw")
    return r.text

def update_dns(ip, host):
    headers = {"Authorization": "sso-key " + key + ":" + secret}
    r = requests.get(base_url + endpoint_a_records + host, headers=headers)

    if r.status_code != 200:
        return r

    records = r.json()
    new_records = [{"data": ip, "name": host, "type": "A"}]

    # Create new DNS Record
    if len(records) == 0:
        print("creating... ", end="")
        return requests.patch(base_url + endpoint_records, json=new_records, headers=headers)
    
    # Replace existing record
    elif len(records) == 1:
        print("updating... ", end="")
        return requests.put(base_url + endpoint_a_records + host, json=new_records, headers=headers)
    
    # Error: More than 1 record on host
    elif len(records) > 1:
        print("[!] You got " + str(len(records)) + " records of type A with host " + host + ". Please delete as least " + str(len(records) - 1) + " of them")

    # Error
    else:
        print(f"[!] Error. Chech DNS records on {host}")

def main():
    print()
    print("### GoDaddy DynDNS ###")
    print()
    print(f"[*] Using config file: {config_file}")

    if watchmode:
        print(f"[*] Watchmode enabled. Update will run every {watchmode_interval} seconds")

    while True:
        last_ip = get_last_ip()
        print(f"[*] Cached IP is: {last_ip}")
        ip = get_ip()
        print(f"[*] Public IP is: {ip}")
        print()

        if ip != last_ip:
            safe_new_ip(ip)
            print(f"[*] Updating hosts {hosts} on {domain} to {ip}")
            print()

            for host in hosts:
                print(f"[*] Processing {host}.{domain} ...", end=" ")

                r = update_dns(ip, host)
                if r is not None and r.status_code == 200:
                    print("Done")
                elif r is not None:
                    print("Error: " + r.text)
        else:
            print("[*] IP hasn't changed. No update.")
        
        if not watchmode:
            return
        
        time.sleep(watchmode_interval)

if __name__ == "__main__":
    main()
