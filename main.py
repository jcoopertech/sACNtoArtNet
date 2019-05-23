import socket
import sACN
import ArtNet
import time
import socket_settings
import threading

'''EXECUTABLE CODE VARS'''
universe_min = 255
universe_max = 256


def calculate_hibit(byte: int):
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


input_data = {}  # Create an empty byte for the merge function
for i in range(universe_max+1):
    uni = calculate_hibit(i)
    input_data[uni[0], uni[1]] = {}


def set_fps(fps=45):
    loop_time = time.time() + (1/fps)
    return loop_time


def clear_dmx_data():
    dmx_data = bytearray()  # Flush DMX data
    for i in range(512):
        dmx_data.append(0)
    return dmx_data


def merge_sacn_inputs(sacn_data):   # Input Universe, CID and DMX data
    output = bytearray()            # Reset DMX output
    for i in range(512):
        output.append(0)
    input_data[sacn_data["universe"]][sacn_data["cid"]] = sacn_data["dmx_data"]  # Store input Universe, CID and DMX
    for cids in input_data[sacn_data["universe"]]:  # Loop for every CID input on this universe
        for dmx_length in range(512):               # Loop for every position of the DMX packet
            if output[dmx_length] < input_data[sacn_data["universe"]][cids][dmx_length]:
                output[dmx_length] = input_data[sacn_data["universe"]][cids][dmx_length]
    sacn_data["dmx_data"] = output
    return sacn_data["dmx_data"], sacn_data["universe"]


def identify_sacn_packet(sacn_input):
    # Extracts the type of sACN packet and will return the type of packet and the packet itself.
    try:
        len(sacn_input) < 126
        if len(sacn_input) < 126:
            raise TypeError("Unknown Package. The minimum length for a sACN package is 126.")
    except TypeError as error_message:
        print("LENGHT ERROR:", error_message)
    if tuple(sacn_input[40:44]) == sACN.VECTOR_E131_DATA_PACKET:     # sACN Data Packet
        sacn_data = sACN.sacn_data_input(sacn_input_packet)     # Extract all data we can get
        sacn_data["dmx_data"], sacn_data["input_data"] = merge_sacn_inputs(sacn_data)
        # Merge DMX data from multiple sources.
        return "sACN_DATA_PACKET", sacn_data
    elif tuple(sacn_input[40:44]) == sACN.VECTOR_E131_EXTENDED_SYNCHRONIZATION:  # sACN Sync Packet
        sacn_sync = sACN.sacn_sync_input(sacn_input_packet)  # Extract all data we can get
        return "sACN_EXTENDED_SYNCHRONIZATION", sacn_sync
    elif tuple(sacn_input[40:44]) == sACN.VECTOR_E131_EXTENDED_DISCOVERY:  # sACN Discovery Packet
        sacn_discovery = sACN.sacn_discovery_input(sacn_input_packet)  # Extract all data we can get
        return "sACN_EXTENDED_DISCOVERY", sacn_discovery


set_acn_sock = socket_settings.sacn_socket_setup("0.0.0.0", universe_min, universe_max)
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
    sACN_data = identify_sacn_packet(sacn_input_packet)            # Identify Packet Type.
    if sACN_data[0] == "sACN_DATA_PACKET":
        ArtNet.artdmx_output(sACN_data[1])          # Send corresponding ArtNet packet.
    elif sACN_data[0] == "sACN_EXTENDED_SYNCHRONIZATION":
        print("Sync Packet detected")
        # ArtNet.artpoll_output(sACN_data[1])         # Send corresponding ArtPoll packet. (<-To Do)
    elif sACN_data[0] == "sACN_EXTENDED_DISCOVERY":
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