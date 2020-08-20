import re
import subprocess


try:
    output = subprocess.check_output(['ipconfig'])
except Exception:
    output = subprocess.check_output(['ifconfig'])

ips = re.findall(
    r'inet (\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})',
    output.decode('utf-8'),
)

for ip in ips:
    if ip.startswith('127'):
        addr_type = 'loopback'
    elif ip.startswith(('192', '172')):
        addr_type = 'private'
    elif '0.0' not in ip:
        addr_type = 'global'
    else:
        addr_type = 'unknown'
    print(ip, addr_type)
