from artnet.artnet_params import *
from load_settings import load_settings


def merge_inputs(artnet_data):
    if load_settings("artnet_to_sacn", "Art-Net") is True:
        if load_settings("merge_artnet", "Art-Net") is True:
            pass  # ToDo


def identify_artnet_packet(packet):
    """Returns the universe_type of Art-Net packet that was received"""
    """INPUT: Art-Net packet"""
    """OUTPUT: Type of packet"""
    if tuple(packet[0:8]) != ID or packet[10] != PROT_VER_HI or packet[11] != PROT_VER_LO:
        return "No Art-Net packet"
    elif packet[8] == OP_POLL[1] and packet[9] == OP_POLL[0]:
        return "ART_POLL"
    elif packet[8] == OP_POLL_REPLY[1] and packet[9] == OP_POLL_REPLY[0]:
        return "ART_POLL_REPLY"
    elif packet[8] == OP_IP_PROG[1] and packet[9] == OP_IP_PROG[0]:
        return "ART_IP_PROG"
    elif packet[8] == OP_IP_PROG_REPLY[1] and packet[9] == OP_IP_PROG_REPLY[0]:
        return "ART_IP_PROG_REPLY"
    elif packet[8] == OP_ADDRESS[1] and packet[9] == OP_ADDRESS[0]:
        return "ART_ADDRESS"
    elif packet[8] == OP_DIAG_DATA[1] and packet[9] == OP_DIAG_DATA[0]:
        return "ART_DIAG_DATA"
    elif packet[8] == OP_TIME_CODE[1] and packet[9] == OP_TIME_CODE[0]:
        return "ART_POLL"
    elif packet[8] == OP_COMMAND[1] and packet[9] == OP_COMMAND[0]:
        return "ART_COMMAND"
    elif packet[8] == OP_TRIGGER[1] and packet[9] == OP_TRIGGER[0]:
        return "ART_TRIGGER"
    elif packet[8] == OP_DMX[1] and packet[9] == OP_DMX[0]:
        return "DMX_PACKET"
    elif packet[8] == OP_SYNC[1] and packet[9] == OP_SYNC[0]:
        return "ART_SYNC"
    elif packet[8] == OP_NZS[1] and packet[9] == OP_NZS[0]:
        if packet[30] == 0x91 and packet[50] == 0x41 and packet[51] == 0x4C and packet[52] == 0x45:
            # <- ToDo, its not 30, 50,51 and 52.
            return "ART_VLC"
        else:
            return "ART_NZS"
    elif packet[8] == OP_INPUT[1] and packet[9] == OP_INPUT[0]:
        return "ART_packet"
    elif packet[8] == OP_FIRMWARE_MASTER[1] and packet[9] == OP_FIRMWARE_MASTER[0]:
        return "ART_FIRMWARE_MASTER"
    elif packet[8] == OP_FIRMWARE_REPLY[1] and packet[9] == OP_FIRMWARE_REPLY[0]:
        return "ART_FIRMWARE_REPLY"
    elif packet[8] == OP_TOD_REQUEST[1] and packet[9] == OP_TOD_REQUEST[0]:
        return "ART_TOD_REQUEST"
    elif packet[8] == OP_TOD_DATA[1] and packet[9] == OP_TOD_DATA[0]:
        return "ART_TOD_DATA"
    elif packet[8] == OP_TOD_CONTROL[1] and packet[9] == OP_TOD_CONTROL[0]:
        return "ART_TOD_CONTROL"
    elif packet[8] == OP_RDM[1] and packet[9] == OP_RDM[0]:
        return "RDM_PACKET"
    elif packet[8] == OP_RDM_SUB[1] and packet[9] == OP_RDM_SUB[0]:
        return "RDM_SUB_PACKET"


def artnet_dmx_input(artnet_packet):
    # If this is a normal DMX packet (Start Code = 0x00)
    # Dictionary with all the information we can get from this package
    artnet_data = {"sequence_number": artnet_packet[12], "physical_port": artnet_packet[13],
                   "universe": tuple(artnet_packet[14:16]), "universe_lobyte": artnet_packet[14],
                   "universe_hibyte": artnet_packet[15], "length": tuple(artnet_packet[16:18]),
                   "dmx_data": artnet_packet[18:530]}
    return artnet_data
