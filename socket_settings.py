import socket
from params import ArtNetParams, sACNParams

'''GLOBAL PARAMS'''
universe_min = 1
universe_max = 20
merge_mode = "HTP"  # Can be "HTP", "LTP" or "DISABLED"
artnet_to_sacn = False
sacn_to_artnet = True
broadcast = True    # Normally, unicast should be used to talk to ArtNet devices. Some old devices don't send ArtPolls,
#                   # so you have to disable unicast and send broadcast.
ip = "0.0.0.0"      # Your IP. Set to "0.0.0.0" to use your device IP

def calculate_multicast_addr(universemin: int):
    hibyte = universemin >> 8
    lobyte = universemin & 0xFF
    return F"239.255.{hibyte}.{lobyte}"


def sacn_socket_setup(udp_ip="127.0.0.1", min_universe=universe_min, max_universe=universe_max,
                      sacn_port=sACNParams.ACN_SDT_MULTICAST_PORT):
    """SACN SOCKET"""
    print("RUNNING sACN SOCKET SETUP...")
    sacn_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Set up socket
    try:
        sacn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reuse address if already taken by another application
    except:
        print(f"Address can't be reused! Please close all applications that are assigned to Port \
        {sacn_port}")
    sacn_sock.bind((udp_ip, sacn_port))     # Calculate multicast addresses and bind to it
    multicast_list = []
    print(f"Listening to sACN on Universe {min_universe} thru {max_universe}")
    while min_universe <= max_universe:
        multicast_list.append(calculate_multicast_addr(min_universe))
        sacn_sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(calculate_multicast_addr(min_universe)) + socket.inet_aton(udp_ip))
        min_universe = min_universe + 1
    print(f"Joined Multicast Group:{multicast_list}")
    print(f"UDP target IP: {udp_ip}")
    print(f"UDP target Port: {sacn_port}")
    return sacn_sock


def artnet_socket_setup(udp_ip="127.0.0.1", artnet_port=ArtNetParams.UDP_PORT):
    """ART-NET SOCKET"""
    print("RUNNING ART-NET SOCKET SETUP...")
    artnet_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Set up socket
    artnet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)  # Broadcast for ArtNet-Broadcast sending
    try:
        artnet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reuse address if already taken by another application
    except:
        print(f"Address can't be reused! Please close all applications that are assigned to Port \
        {artnet_port}")
    artnet_sock.bind((udp_ip, artnet_port))  # Calculate multicast addresses and bind to it
    print(f"UDP target IP: {udp_ip}")
    print(f"UDP target Port: {artnet_port}")
    return artnet_sock
