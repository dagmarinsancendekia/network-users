from flask import Flask, render_template
import subprocess
import ipaddress
import socket
import re
import concurrent.futures

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

def ping_ip(ip):
    """Ping a single IP address."""
    import platform
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    result = subprocess.run(['ping', param, '1', timeout_param, '1', str(ip)], capture_output=True)
    return result.returncode == 0

def ping_sweep(subnet):
    """Perform parallel ping sweep on the subnet to populate ARP table."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping_ip, ip): ip for ip in subnet.hosts()}
        for future in concurrent.futures.as_completed(futures):
            pass  # Just to wait for completion

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
