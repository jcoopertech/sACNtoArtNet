import socket
from load_settings import load_settings


def calculate_hibyte(byte: int):
    """Returns a list with the hibyte[0] and the lobyte[1]
    Input: Integer
    Output: 2 Byte List"""
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


"""VARS"""
merge_dict = {}  # Create an empty input_dict for the merge function
for universes in range(len(load_settings("sacndict"))+1):
    universe = calculate_hibyte(universes)
    merge_dict[universe[0], universe[1]] = {}


"""SETUP"""


def calculate_multicast_address(universe):
    """Calcutates the multicast address assigned to the input universe"""
    """Input: Universe"""
    """Output: Universe Multicast Address"""
    hibyte = universe >> 8
    lobyte = universe & 0xFF
    return f"239.255.{hibyte}.{lobyte}"


def set_sacn_socket(ip=load_settings("ip", "sACN"), sacn_port=load_settings("sacn_port", "sACN")):
    """sACN SOCKET"""
    print("RUNNING sACN SOCKET SETUP...")
    sacn_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Set up socket
    try:
        sacn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reuse address if already taken by another application
    except RuntimeWarning:
        print(f"Address can't be reused! Please close all applications that are assigned to Port \
            {sacn_port}")
    sacn_sock.bind((ip, sacn_port))  # Calculate multicast addresses and bind to it
    for universe in load_settings("sacndict", "sACN"):
        sacn_sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(calculate_multicast_address(universe)) + socket.inet_aton(ip))
    print(f"sACN target IP: {ip}")
    print(f"sACN target Port: {sacn_port}")
    return sacn_sock


sacn_socket = set_sacn_socket()
