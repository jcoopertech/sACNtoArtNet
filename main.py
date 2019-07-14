import socket
import sACN
import ArtNet
import socket_settings
from params.UserParams import *
from params.sACNParams import *

"""SETUP"""
# Set up Socket for ArtNet and sACN
set_acn_sock = socket_settings.sacn_socket_setup(socket_settings.ip)
set_artnet_sock = socket_settings.artnet_socket_setup(socket_settings.ip)


while True:
    if sacn_to_artnet is True and artnet_to_sacn is True:
        raise RuntimeError("Both conversion directions are enabled! Disable one conversion direction")

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
                sACN.add_sacn_priority(sACN_data)
                # If the START_CODE is 0xDD, update the Priority for the universe
            elif sACN_start_code == "RDM":
                pass  # ToDo for when E1.33 is published
            elif sACN_start_code == "ALTERNATE":
                ArtNet.artnzs_output(sACN_data)
                # If the START_CODE is alternating, send a Non-Zero-Start-Code packet.

        elif sACN_packet_type == "sACN_EXTENDED_SYNCHRONIZATION":
            if debug_level >= 4:
                print(f"{sACN_packet_type}") # ToDo
        elif sACN_packet_type == "sACN_EXTENDED_DISCOVERY":
            if debug_level >= 4:
                print(f"{sACN_packet_type}") # ToDo

        '''Receive ArtNet Poll packets and send corresponding ArtNet Poll Reply packets'''
        try:
            artnet_input_packet, artnet_ip_input = set_artnet_sock.recvfrom(1143)
            # Don't know what the maximum length is yet. <- ToDo
        except socket.timeout:
            if debug_level >= 1:
                print("Timeout")
            continue
        artnet_data = ArtNet.identify_artnet_packet(artnet_input_packet)

    elif artnet_to_sacn is True:
        pass