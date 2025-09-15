from flask import Flask, render_template
import subprocess
import ipaddress
import socket
import re

app = Flask(__name__)

def get_local_ip():
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_subnet(ip):
    """Get the subnet from IP address, assuming /24."""
    return ipaddress.ip_network(ip + '/24', strict=False)

def ping_sweep(subnet):
    """Perform ping sweep on the subnet to populate ARP table."""
    for ip in subnet.hosts():
        subprocess.run(['ping', '-n', '1', '-w', '100', str(ip)], capture_output=True)

def get_arp_table():
    """Retrieve the ARP table and parse devices."""
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    devices = []
    for line in lines:
        parts = re.split(r'\s+', line.strip())
        if len(parts) >= 3 and parts[0] != 'Interface:' and '.' in parts[0]:
            ip = parts[0]
            mac = parts[1]
            devices.append({'ip': ip, 'mac': mac})
    return devices

@app.route('/')
def index():
    local_ip = get_local_ip()
    subnet = get_subnet(local_ip)
    ping_sweep(subnet)
    devices = get_arp_table()
    return render_template('index.html', devices=devices)

if __name__ == '__main__':
    app.run(debug=True)
