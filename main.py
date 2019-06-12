import socket
import sACN
import ArtNet
import time
import socket_settings
from params.UserParams import *


def set_fps(fps=45):
    loop_time = time.time() + (1/fps)
    return loop_time


def clear_dmx_data():
    dmx_data = bytearray()  # Flush DMX data
    for i in range(512):
        dmx_data.append(0)
    return dmx_data


set_acn_sock = socket_settings.sacn_socket_setup(socket_settings.ip)
set_artnet_sock = socket_settings.artnet_socket_setup(socket_settings.ip)
# IP: Set your own IP. Set to "0.0.0.0" to assign it automatically.
# Universe Minimum: First Universe in a range to listen to.
# Universe Maximum: Last Universe in a range to listen to.
while True:
    if sacn_to_artnet is True:
        '''Receive sACN packets and send corresponding ArtNet packet'''
        try:
            sacn_input_packet, sacn_ip_input = set_acn_sock.recvfrom(1143)  # 1143 is the max length of a sACN packet.
        except socket.timeout:  # If timeout, continue
            if debug_level >= 1:
                print("Timeout")
            continue
        packet_type, sACN_data = sACN.identify_sacn_packet(sacn_input_packet)            # Identify Packet Type.
        if packet_type == "sACN_DATA_PACKET":
            ArtNet.artdmx_output(sACN_data)          # Send corresponding ArtNet packet.
            if debug_level >= 4:
                print(f"{packet_type}")
        elif packet_type == "sACN_EXTENDED_SYNCHRONIZATION":
            if debug_level >= 4:
                print(f"{packet_type}")
            ArtNet.artpoll_output()         # Send corresponding ArtPoll packet. <-ToDo
        elif packet_type == "sACN_EXTENDED_DISCOVERY":
            if debug_level >= 4:
                print(f"{packet_type}")
            # ArtNet.artpollreply_output(sACN_data[1])    # Send corresponding ArtPollReply packet. <-ToDo

        '''Receive ArtNet Poll packets and send corresponding ArtNet Poll Reply packets'''
        try:
            artnet_input_packet, artnet_ip_input = set_artnet_sock.recvfrom(1143)
            # Don't know what the maximum length is yet. <- ToDo
        except socket.timeout:
            if debug_level >= 1:
                print("Timeout")
            continue
        artnet_data = ArtNet.identify_artnet_packet(artnet_input_packet)

    if artnet_to_sacn is True:
        try:
            artnet_input_packet, artnet_ip_input = set_artnet_sock.recvfrom(1143)
            # Don't know what the maximum length is yet. <- ToDo
        except socket.timeout:
            if debug_level >= 1:
                print("Timeout")
            continue
        artnet_data = ArtNet.identify_artnet_packet(artnet_input_packet)
