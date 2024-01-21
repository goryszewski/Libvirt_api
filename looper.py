import time

from lib.Libvirt import Libvirt

conn = Libvirt()

import requests

url = "http://api:5000/api/vms"



while True:
    vms = conn.get()
    for vm in vms:
        data = {
            "name": vm['name'],
            "cpu": vm['info'][1],
            "memory": vm['info'][3],
            "status":vm['status']
            }
        print(data)

        response = requests.post(url, json=data)
        print(response)
    time.sleep(10)
