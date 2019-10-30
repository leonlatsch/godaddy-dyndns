#!/usr/bin/python3

# MIT License
# 
# Copyright (c) 2019 Leon Latsch

from configparser import ConfigParser
import requests
import json
import os

cfg = ConfigParser()
cfg.read(os.path.dirname(__file__) + "/godaddy-dyndns.conf")

key = cfg.get("godaddy", "key")
secret = cfg.get("godaddy", "secret")
domain = cfg.get("godaddy", "domain")

base_url = "https://api.godaddy.com"
endpoint_update = "/v1/domains/" + domain + "/records"
endpoint_records = "/v1/domains/" + domain + "/records/A/@"

def get_ip():
    r = requests.get("https://api.ipify.org/?format=raw")
    if r.status_code != 200: # Fallback
        r = requests.get("http://ip.42.pl/raw")
    return r.text

def update_dns(ip):
    headers = {"Authorization": "sso-key " + key + ":" + secret}
    r = requests.get(base_url + endpoint_records, headers=headers)

    if r.status_code != 200:
        return r
    
    records = r.json()
    new_records = [{"data": ip, "name": "@", "type": "A"}]

    if len(records) == 0:
        return requests.patch(base_url + endpoint_update, json=new_records, headers=headers)
    elif len(records) == 1:
        return  requests.put(base_url + endpoint_records, json=new_records, headers=headers)
    elif len(records) > 1:
        print("[!] You got " + str(len(records)) + " records of type A with host @. Please delete as least " + str(len(records) - 1) + " of them")
        

ip = get_ip()
r = update_dns(ip)
if r is not None and r.status_code == 200:
    print("[*] Updated dns record for " + domain + " to " + ip)
elif r is not None:
    print("[!] Error updating dns record: " + str(r.status_code) + " " + str(r.reason))
