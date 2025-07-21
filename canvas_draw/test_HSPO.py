import socket
import struct

from recv import run_canvas_gui


# def hspo_extract(data):
#     binary_format = ">LLLHH6fLL"  # Adjust if your format changes
#     required_length = struct.calcsize(binary_format)

#     if len(data) >= required_length:
#         unpacked = struct.unpack(binary_format, data[:required_length])
#         X, Y, Z = unpacked[5], unpacked[6], unpacked[7]
#         W, P, R = unpacked[8], unpacked[9], unpacked[10]
#         return X, Y, Z, W, P, R
#     else:
#         print("Packet too short for expected format")
#         return None

def main():
    UDP_IP = "0.0.0.0"  # Listen on all interfaces
    UDP_PORT = 31001     # Replace with your actual HSPO port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(2.0)  # Optional timeout
    
    print(f"Listening for HSPO I data on {UDP_IP}:{UDP_PORT}...")
    try:
        run_canvas_gui(sock)
    except KeyboardInterrupt:
        print("Test stopped by user.")
    finally:
        sock.close()
       

main()