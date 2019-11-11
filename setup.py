import socket_settings

'''SETUP'''


def calculate_hibit(byte: int):
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


"""SOCKET SETUP"""
# Set up Socket for ArtNet and sACN
set_acn_sock = socket_settings.sacn_socket_setup(socket_settings.ip)
set_artnet_sock = socket_settings.artnet_socket_setup(socket_settings.ip)
set_artnet_unicast_sock = socket_settings.artnet_socket_unicast_setup(socket_settings.ip)

"""SACN SETUP"""
universe_shift = {}  # Create an empty dict for the shift function
merge_dict = {}  # Create an empty dict for the merge function
for universes in range(len(socket_settings.universe_dict) + 1):  # It is as long as the highest possible universe.
    universe = calculate_hibit(universes)
    merge_dict[universe[0], universe[1]] = {}

"""ARTNET SETUP"""
unicast_ips = {}
delete_list = {}
