#!/usr/bin/env python3

from contextlib import contextmanager
import pifacecad
import time

from pollers import poll_pi, ButtonPoller
from collector import SysValues

cad = pifacecad.PiFaceCAD()
HOSTS_FILE = 'hosts.txt'

def get_hosts(f):
    with open(f, 'r') as hosts_file:
        return [line.rstrip() for line in hosts_file]

def format_values(hostname, values=None):
    if values is not None:
        return '{}: cpu={}%\ndisk={}%, ram={}%'.format(
                hostname, *values)
    else:
        return 'Could not reach\nhost "{}"'.format(hostname)

@contextmanager
def display_manager():
    cad.lcd.display_on()
    cad.lcd.clear()
    cad.lcd.backlight_on()
    yield
    for _ in range(20): 
        cad.lcd.move_left()
        time.sleep(1)
    cad.lcd.backlight_off()
    cad.lcd.clear()
    cad.lcd.display_off()

def main():
    all_hosts = get_hosts(HOSTS_FILE)
    buttons = ButtonPoller(cad)
    while True:
        pressed_button = buttons.poll()
        if pressed_button is not False and pressed_button < len(all_hosts):
            with display_manager():
                host = all_hosts[pressed_button]
                data = poll_pi(host)
                if data is not None:
                    data = SysValues(**data)
                text = format_values(host, data)
                cad.lcd.write(text)
        time.sleep(1)

if __name__ == '__main__':
    main()
