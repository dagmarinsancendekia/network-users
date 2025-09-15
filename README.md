# Network Users App

A simple Flask web application that scans and displays devices connected to the local wireless network.

## Features
- Scans the local subnet for connected devices using ping sweep.
- Displays IP addresses and MAC addresses of discovered devices.
- Web-based interface for easy viewing.

## Requirements
- Python 3.x
- Flask

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/dagmarinsancendekia/network-users.git
   cd network-users
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python app.py
   ```

2. Open a web browser and go to `http://127.0.0.1:5000/`

3. The app will scan the network and display the list of devices.

## Note
- The app assumes a /24 subnet. Adjust the subnet calculation in `app.py` if needed.
- Scanning may require administrative privileges on some systems.
- This app performs a basic ping sweep and ARP table lookup. For more advanced scanning, consider using tools like nmap.

## License
MIT License
