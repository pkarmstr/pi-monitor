import requests

POLL_PORT = 6649

def poll_pi(hostname):
    resp = requests.get('http://{}:{}'.format(hostname, POLL_PORT))
    return resp.json() if resp.status_code == 200 else {}

class ButtonPoller:
    def __init__(self, cad):
        self.buttons = cad.switches

    def poll(self):
        for i, b in enumerate(self.buttons):
            if b.value == 1:
                return i
        return False
