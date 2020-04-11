from sacn.sacn_params import *
from uuid import uuid5, NAMESPACE_DNS
from load_settings import load_settings
from sacn.sacn_socket import sacn_socket


def calculate_multicast_address(universe):
    """Calcutates the multicast address assigned to the input universe"""
    """Input: Universe"""
    """Output: Universe Multicast Address"""
    hibyte = universe >> 8
    lobyte = universe & 0xFF
    return f"239.255.{lobyte}.{hibyte}"


def calculate_hibyte(byte: int):
    """Returns a list with the hibyte[0] and the lobyte[1]
    Input: Integer
    Output: 2 Byte List"""
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


def calculate_decimal(byte_input):
    """Returns an int from a list of bytes
    Input: Tuple/List (Hibyte, Lobyte)
    Output: Int"""
    result = (byte_input[0] << 8) + byte_input[1]  # Converts a tuple back to an int
    return result


def calculate_flags_and_length(length, position):
    """Returns the flags and length bytes
    Input: Length (Dec), Position of the octet in the transmitted data
    Output: 2 Bytes (flags and length)"""
    length = length - position
    hibyte = ((0x70 << 8) + (length & 0xF00) >> 8)
    lobyte = (length & 0xFF)
    return hibyte, lobyte


def calculate_cid(source_name="Area31"):
    """Calculate a CID based on the mac address of the device
    Input: Name of the source, if given
    Output: CID"""
    cid = uuid5(NAMESPACE_DNS, f"{source_name}")
    return cid.bytes


def calculate_fill_characters(string, length=64):
    """Output a string with fill characters, if it is too short
    Input: String, Target length
    Output: String with target length"""
    output = string.ljust(length)[:length]  # <- ToDo: Should not be space, 0x00 instead
    return bytes(output, "ascii")


sequence = 0


def sacn_dmx_output(sacn_data, preview_data=0, stream_terminated=0, force_synchronisation=0):
    # E131 Data Packet:
    # # # ROOT LAYER # # #
    # 0-1:      Preamble Size (0x0010)                                        <- Discard if not valid
    # 2-3:      Postable Size (0x0000)                                        <- Discard if not valid
    # 4-15:     ACN Packet Identifier
    #           (0x41 0x53 0x43 0x2d 0x45 0x31 0x2e 0x31 0x37 0x00 0x00 0x00) <- Discard if not valid
    # 16-17:    Flags and length (Low 12 bits = PDU length, High 4 bits = 0x7)
    # 18-21:    Identifies RLP Data as 1.31 Protocol
    #           (VECTOR_ROOT_E131_DATA or VECTOR_ROOT_E131_EXTENDED)          <- Discard if not valid
    # 22-37:    Senders unique CID
    # # # DATA PACKET FRAMING LAYER # # #
    # 38-39     Flags and lenght (Low 12 bits = PDU length, High 4 bits = 0x7
    # 40-43     Identifies 1.31 data as DMP Protocol PDU (VECTOR_E131_DATA_PACKET)
    # 44-107:   Source Name assigned by User (UTF-8 encoded string)
    # 108:      Package Priority of multiple sources (0-200, 100 being default)
    # 109-110:  Synchronization Address (Universe on which sync packets will be sent)
    # 111:      Sequence Number (To detect duplicate or out of order packets)
    # 112:      Options (Bit 5 = Force_Synchronization, Bit 6 = Stream_Terminated, Bit 7 = Preview Data)
    # 113-114:  Universe Number
    # # # DMP Layer # # #
    # 115-116:  Flags and length (Low 12 bits = PDU Length, High 4 bits = 0x7)
    # 117:      Identifies DMP Set Property Message PDU (VECTOR_DMP_SET_PROPERTY) <- Discard if not valid
    # 118:      Address Type and Data Type (0xa1)                                 <- Discard if not valid
    # 119-120:  First property address, Indicates DMX Start Code is at DMP address 0 (0x0000)   <- Discard if not valid
    # 121-122:  Address Increment, Indicate each property is 1 octet (0x0001)     <- Discard if not valid
    # 123-124:  Property value count, Indicates +1 the number of slots in packet (0x0001 -- 0x0201)
    # 125-637:  Property values, DMX Start Code and data (Start Code + data)                        <- DMX DATA

    packet_length = (126 + len(sacn_data["dmx_data"]))

    # CID
    if "short_name" in sacn_data:
        cid = calculate_cid(sacn_data["short_name"])
    else:
        cid = calculate_cid()  # If source has no name, use a standard one

    # Source Name
    if "long_name" in sacn_data:
        source_name = calculate_fill_characters(sacn_data["long_name"], 64)  # <- ToDo
    else:
        source_name = calculate_fill_characters("Area 31", 64)

    # Options
    options = int(f"{preview_data}{stream_terminated}{force_synchronisation}00000", 2)

    # Length
    length = (calculate_decimal(sacn_data["length"]) + 1)  # Add one, since the start code is counted as length
    length = calculate_hibyte(length)

    # Sequence
    if sacn_data["sequence_number"] == 0:
        # While the sequence number can be disabled in Art-Net, it is needed in Art-Net. Adding a sequence number for
        # every packet if needed
        global sequence
        sequence += 1
        if sequence > 255:
            sequence = 0
    else:
        sequence = sacn_data["sequence_number"]  # Take original sequence number, if possible

    # # # ROOT LAYER # # #
    sacn_packet = bytearray()
    sacn_packet.extend(PREAMBLE_SIZE)
    sacn_packet.extend(POST_AMBLE_SIZE)
    sacn_packet.extend(ACN_PACKET_IDENTIFIER)
    sacn_packet.extend(calculate_flags_and_length(packet_length, 16))  # Flags and length hibyte
    sacn_packet.extend(VECTOR_ROOT_E131_DATA)
    sacn_packet.extend(cid)
    # # # DATA PACKET FRAMING LAYER # # #
    sacn_packet.extend(calculate_flags_and_length(packet_length, 38))
    sacn_packet.extend(VECTOR_E131_DATA_PACKET)
    sacn_packet.extend(source_name)
    sacn_packet.append(load_settings("artnet_priority", "Art-Net"))
    sacn_packet.append(0x0)  # <- ToDo: Synchronisation Address
    sacn_packet.append(0x0)
    sacn_packet.append(sequence)
    sacn_packet.append(options)
    sacn_packet.append(sacn_data["universe_hibyte"])
    sacn_packet.append(sacn_data["universe_lobyte"])
    # # # DMP LAYER # # #
    sacn_packet.extend(calculate_flags_and_length(packet_length, 115))
    sacn_packet.append(VECTOR_DMP_SET_PROPERTY)
    sacn_packet.append(0xA1)
    sacn_packet.extend((0x00, 0x00))
    sacn_packet.extend((0x00, 0x01))
    sacn_packet.extend(length)  # Length of the dmx data plus start code
    sacn_packet.append(0x00)  # DMX Start code
    sacn_packet.extend(sacn_data["dmx_data"])  # DMX data

    sacn_output(sacn_packet, calculate_multicast_address(calculate_decimal(list(sacn_data["universe"]))))


def sacn_output(sacn_packet, target_ip):
    try:
        sacn_socket.sendto(sacn_packet, (target_ip, load_settings("sacn_port", "sACN")))
    except Exception as exception:
        print(f"Socket error: {exception}")