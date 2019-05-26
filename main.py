import socket
import sACN
import ArtNet
import time
import socket_settings
import threading




def set_fps(fps=45):
    loop_time = time.time() + (1/fps)
    return loop_time


def clear_dmx_data():
    dmx_data = bytearray()  # Flush DMX data
    for i in range(512):
        dmx_data.append(0)
    return dmx_data


set_acn_sock = socket_settings.sacn_socket_setup("0.0.0.0", socket_settings.universe_min, socket_settings.universe_max)
set_artnet_sock = socket_settings.artnet_socket_setup("0.0.0.0")
# IP: Set your own IP. Set to "0.0.0.0" to assign it automatically.
# Universe Minimum: First Universe in a range to listen to.
# Universe Maximum: Last Universe in a range to listen to.
while True:
    '''Receive sACN packets and send corresponding ArtNet packet'''
    try:
        sacn_input_packet, sacn_ip_input = set_acn_sock.recvfrom(1143)  # 1143 is the maximum length of a sACN packet.
    except socket.timeout:                                    # If timeout, continue
        print("Timeout")
        continue
    packet_type, sACN_data = sACN.identify_sacn_packet(sacn_input_packet)            # Identify Packet Type.
    if packet_type == "sACN_DATA_PACKET":
        ArtNet.artdmx_output(sACN_data)          # Send corresponding ArtNet packet.
    elif packet_type == "sACN_EXTENDED_SYNCHRONIZATION":
        print("Sync Packet detected")
        ArtNet.artpoll_output()         # Send corresponding ArtPoll packet. (<-To Do)
    elif packet_type == "sACN_EXTENDED_DISCOVERY":
        print("Discovery Packet detected")
        # ArtNet.artpollreply_output(sACN_data[1])    # Send corresponding ArtPollReply packet. (<-To Do)

    '''Receive ArtNet packets and send corresponding sACN packets'''
    try:
        artnet_input_packet, artnet_ip_input = set_artnet_sock.recvfrom(1143)
        # Don't know what the maximum length is yet. <- To Do
    except socket.timeout:
        print("Timeout")
        continue
    artnet_data = ArtNet.identify_artnet_packet(artnet_input_packet)
