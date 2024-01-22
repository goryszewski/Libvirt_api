import time

from lib.Libvirt import Libvirt

conn = Libvirt()

import requests

from util.env import get_env

url = f"http://{get_env('api')}:{get_env('port')}"



while True:

    ### Begin Inventory
    vms = conn.get()
    for vm in vms:
        data = {
            "name": vm['name'],
            "cpu": vm['info'][1],
            "memory": vm['info'][3],
            "status":vm['status']
            }
        response = requests.post(f"{url}/api/vms", json=data)

    ### Begin Tasks

    response = requests.get(f"{url}/api/tasks")
    tasks = response.json()

    for task in tasks:
        task_status={"status":0,"payload":"done"}

        response = requests.post(f"{url}/api/task/{task['id']}", json=task_status)

    time.sleep(30)
