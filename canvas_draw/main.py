import socket
from HSPO_extract import hspo_extract
from move_robot import FRC_methods
import struct
from canvas_draw import run_canvas_gui  # Import the function you just created

# initialize sockets
def tcp_connect():
    ip_connect = "192.168.1.100"
    port_connect = 16002
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_connect, port_connect))
    s.settimeout(1) # Set a timeout for the socket operations
    return s

def udp_client():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 31001
    u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    u.bind((UDP_IP, UDP_PORT))
    u.settimeout(2.0)
    return u
    
# Create an instance of the class
HSPO = udp_client()
method = FRC_methods(tcp_connect())
method.FRC_connect()
method.FRC_initialize()
method.FRC_reset()


# Start the canvas app and pass the method object
run_canvas_gui(method, HSPO)
