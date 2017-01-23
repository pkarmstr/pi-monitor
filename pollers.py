import requests

POLL_PORT = 6649

def poll_pi(hostname):
    resp = requests.get('http://{}:{}'.format(hostname, POLL_PORT))
    return resp.json() if resp.status_code == 200 else {}

