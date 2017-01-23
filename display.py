#!/usr/bin/env python3

from contextlib import contextmanager
import pifacecad
import time

from poller import poll_pi
from collector import SysValues

cad = pifacecad.PiFaceCAD()
HOSTS_FILE = 'hosts.txt'

def get_hosts(f):
    with open(f, 'r') as hosts_file:
        return [line.rstrip() for line in hosts_file]

def format_values(hostname, values):
    if len(values) > 0:
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
    hosts = get_hosts(HOSTS_FILE)
    while True:
        if cad.switches[0].value == 1:
            with display_manager():
                values = SysValues(**poll_pi('localhost'))
                text = format_values('localhost', values)
                cad.lcd.write(text)

if __name__ == '__main__':
    main()
