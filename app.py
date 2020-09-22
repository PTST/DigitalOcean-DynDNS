import logging
logging.basicConfig(level=logging.INFO)
import os
import requests
from time import sleep
from datetime import datetime


TOKEN = os.environ["DO_TOKEN"]
BASE_URL = os.environ["BASE_URL"]
HOSTNAME = os.environ["HOST_NAME"]
UPDATE_INTERVAL = int(os.environ["UPDATE_INTERVAL"])

CURRENT_IP = ""
LAST_UPDATED = datetime.utcnow()

import logging
import requests

class DigitalOcean(object):
    def __init__(self, token, base_url, hostname):
        self.do_url = "https://api.digitalocean.com/v2/domains"
        self.token = f"Bearer {token}"
        self.base_url = base_url
        self.hostname = f"{hostname}.{base_url}"
        if hostname == "@":
            self.hostname = base_url
    
    def get_record(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.token
        }
        params = {
            "name": self.hostname,
            "type": "A"
        }
        r = requests.get(f"{self.do_url}/{self.base_url}/records", params=params, headers=headers)
        r.raise_for_status()
        obj = r.json()["domain_records"]
        if len(obj) == 0:
            raise Exception("Could not find domain")
        if len(obj) > 1:
            raise Exception("More than one domain returned for query")
        
        return obj[0]

    def update_ip(self, new_ip):
        cur_obj = self.get_record()
        if cur_obj["data"] == new_ip:
            return
        data = {
            "data": new_ip
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.token
        }
        r = requests.put(f"{self.do_url}/{self.base_url}/records/{cur_obj['id']}", json=data, headers=headers)
        r.raise_for_status()
        logging.info(f"IP updated to '{new_ip}'")

client = DigitalOcean(TOKEN, BASE_URL, HOSTNAME)

while True:
    try:
        external_ip = requests.get('https://ipinfo.io/ip').text.strip()
        if external_ip != CURRENT_IP:
            client.update_ip(external_ip)
            CURRENT_IP = external_ip
            LAST_UPDATED = datetime.utcnow()
        
        elif ((datetime.utcnow()-LAST_UPDATED).total_seconds() / 60 )>= 60:
            client.update_ip(external_ip)
            CURRENT_IP = external_ip
            LAST_UPDATED = datetime.utcnow()

    except Exception as e:
        logging.exception(e)
    finally:
        sleep(UPDATE_INTERVAL)
