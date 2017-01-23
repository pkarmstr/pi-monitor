from collections import namedtuple
from psutil import cpu_percent, disk_usage, virtual_memory

SysValues = namedtuple(
    'SysValues', ['cpu_percent', 'disk_usage', 'ram_percent']
)

def collect():
    cpu = cpu_percent()
    disk = disk_usage("/").percent
    mem = virtual_memory().percent
    return SysValues(cpu, disk, mem)
