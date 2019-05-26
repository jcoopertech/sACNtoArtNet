import socket
import sACN
import ArtNetParams


'''GLOBAL PARAMS'''
universe_min = 1
universe_max = 256

'''SACN SOCKET'''
def sacn_socket_setup(UDP_IP="127.0.0.1", universe_min=1, universe_max=1, sacn_port=sACN.ACN_SDT_MULTICAST_PORT):
    sacn_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Set up socket
    try:
        sacn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reuse address if already taken by another application
    except:
        print(f"Address can't be reused! Please close all applications that are assigned to Port \
        {sacn_port}")
    sacn_sock.bind((UDP_IP, sacn_port))     # Calculate multicast addresses and bind to it
    multicast_list = []
    print(f"Listening to sACN on Universe {universe_min} thru {universe_max}")
    while universe_min <= universe_max:
        multicast_list.append(sACN.calculate_multicast_addr(universe_min))
        sacn_sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(sACN.calculate_multicast_addr(universe_min)) + socket.inet_aton(UDP_IP))
        universe_min = universe_min + 1
    print(f"Joined Multicast Group:{multicast_list}")
    print(f"UDP target IP: {UDP_IP}")
    print(f"UDP target Port: {sacn_port}")
    return sacn_sock


'''ART-NET SOCKET'''
def artnet_socket_setup(UDP_IP="127.0.0.1", artnet_port=ArtNetParams.UDP_PORT):
    artnet_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Set up socket
    artnet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)  # Broadcast for ArtNet-Broadcast sending
    try:
        artnet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reuse address if already taken by another application
    except:
        print(f"Address can't be reused! Please close all applications that are assigned to Port \
        {artnet_port}")
    artnet_sock.bind((UDP_IP, artnet_port))  # Calculate multicast addresses and bind to it
    return artnet_sock


set_artnet_sock = artnet_socket_setup("0.0.0.0")
