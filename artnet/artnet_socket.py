import socket
from load_settings import load_settings

"""VARS"""
unicast_ips = {}

"""SETUP"""


def set_artnet_broadcast_socket(ip=load_settings("ip", "Art-Net"), artnet_port=load_settings("artnet_port", "Art-Net")):
    """ART-NET SOCKET"""
    print("RUNNING ART-NET BROADCAST SOCKET SETUP...")
    artnet_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Set up socket
    artnet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)  # Broadcast for ArtNet-Broadcast sending
    artnet_sock.setblocking(False)
    try:
        artnet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reuse address if already taken by another application
    except OSError:
        print(f"Address can't be reused! Please close all applications that are assigned to Port {artnet_port}")
    artnet_sock.bind((ip, artnet_port))
    print(f"Art-Net Broadcast target Port: {artnet_port}")
    return artnet_sock


def set_artnet_unicast_socket(ip=load_settings("ip", "Art-Net"), artnet_port=load_settings("artnet_port", "Art-Net")):
    """ART-NET SOCKET"""
    print("RUNNING ART-NET UNICAST SOCKET SETUP...")
    artnet_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Set up socket
    artnet_sock.setblocking(False)
    try:
        artnet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reuse address if already taken by another application
    except OSError:
        print(f"Address can't be reused! Please close all applications that are assigned to Port {artnet_port}")
    artnet_sock.bind((ip, artnet_port))
    print(f"Artnet Unicast target IP: {ip}")
    print(f"Artnet Unicast target Port: {artnet_port}")
    return artnet_sock


artnet_broadcast_socket = set_artnet_broadcast_socket()
artnet_unicast_socket = set_artnet_unicast_socket()
