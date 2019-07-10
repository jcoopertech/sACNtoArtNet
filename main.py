import socket
import sACN
from params.sACNParams import *
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
# Setting up Socket for ArtNet and sACN

while True:
    if sacn_to_artnet is True:
        '''Receive sACN packets and send corresponding ArtNet packet'''
        try:
            sacn_input_packet, sacn_ip_input = set_acn_sock.recvfrom(1143)  # 1143 is the max length of a sACN packet.
        except socket.timeout:  # If timeout, continue
            if debug_level >= 1:
                print("Timeout")
            continue
        sACN_packet_type = sACN.identify_sacn_packet(sacn_input_packet)
        if sACN_packet_type == "sACN_DATA_PACKET":
            sACN_start_code = sACN.identify_sacn_startcode(sacn_input_packet)
            if debug_level >= 4:
                print(f"{sACN_packet_type} with start code {sACN_start_code}")
            # If it is a DATA_PACKET check the start code.
            sACN.sacn_data_check_validity(sacn_input_packet)  # Check if the data packet is valid

            if sACN_start_code == "DMX":
                sACN_data = sACN.sacn_dmx_input(sacn_input_packet)
                sACN_data["dmx_data"] = sACN.merge_sacn_inputs(sACN_data)
                ArtNet.artdmx_output(sACN_data)
                # If the START_CODE is 0x00, send DMX
            elif sACN_start_code == "PER_CHANNEL_PRIORITY":
                sACN_data = sACN.sacn_per_channel_input(sacn_input_packet)
                sACN_data["priority"] = sACN.add_sacn_priority(sACN_data)
                sACN_data["dmx_data"] = sACN.merge_sacn_inputs(sACN_data)
                ArtNet.artdmx_output(sACN_data)
                # If the START_CODE is 0xDD, update the Priority for the universe
            elif sACN_start_code == "RDM":
                pass  # ToDo
            elif sACN_start_code == "ALTERNATE":
                ArtNet.artnzs_output(sACN_data)
                # If the START_CODE is alternating, send a Non-Zero-Start-Code packet.

        elif sACN_packet_type == "sACN_EXTENDED_SYNCHRONIZATION":
            if debug_level >= 4:
                print(f"{sACN_packet_type}")
            pass  # ToDo
        elif sACN_packet_type == "sACN_EXTENDED_DISCOVERY":
            if debug_level >= 4:
                print(f"{sACN_packet_type}")
            pass  # ToDo

        '''Receive ArtNet Poll packets and send corresponding ArtNet Poll Reply packets'''
        try:
            artnet_input_packet, artnet_ip_input = set_artnet_sock.recvfrom(1143)
            # Don't know what the maximum length is yet. <- ToDo
        except socket.timeout:
            if debug_level >= 1:
                print("Timeout")
            continue
        artnet_data = ArtNet.identify_artnet_packet(artnet_input_packet)

# while True:
#     if sacn_to_artnet is True:
#         '''Receive sACN packets and send corresponding ArtNet packet'''
#         try:
#             sacn_input_packet, sacn_ip_input = set_acn_sock.recvfrom(1143)  # 1143 is the max length of a sACN packet.
#         except socket.timeout:  # If timeout, continue
#             if debug_level >= 1:
#                 print("Timeout")
#             continue
#         packet_type, sACN_data = sACN.identify_sacn_packet(sacn_input_packet)            # Identify Packet Type.
#         if packet_type == "sACN_DATA_PACKET":
#             ArtNet.artdmx_output(sACN_data)          # Send corresponding ArtNet packet.
#             if debug_level >= 4:
#                 print(f"{packet_type}")
#         elif packet_type == "sACN_EXTENDED_SYNCHRONIZATION":
#             if debug_level >= 4:
#                 print(f"{packet_type}")
#             # ArtNet.artpoll_output()         # Send corresponding ArtPoll packet. <-ToDo
#         elif packet_type == "sACN_EXTENDED_DISCOVERY":
#             if debug_level >= 4:
#                 print(f"{packet_type}")
#             # ArtNet.artpollreply_output(sACN_data[1])    # Send corresponding ArtPollReply packet. <-ToDo
#
#         '''Receive ArtNet Poll packets and send corresponding ArtNet Poll Reply packets'''
#         try:
#             artnet_input_packet, artnet_ip_input = set_artnet_sock.recvfrom(1143)
#             # Don't know what the maximum length is yet. <- ToDo
#         except socket.timeout:
#             if debug_level >= 1:
#                 print("Timeout")
#             continue
#         artnet_data = ArtNet.identify_artnet_packet(artnet_input_packet)
#
#     if artnet_to_sacn is True:
#         try:
#             artnet_input_packet, artnet_ip_input = set_artnet_sock.recvfrom(1143)
#             # Don't know what the maximum length is yet. <- ToDo
#         except socket.timeout:
#             if debug_level >= 1:
#                 print("Timeout")
#             continue
#         artnet_data = ArtNet.identify_artnet_packet(artnet_input_packet)
