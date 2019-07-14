from params.sACNParams import *
import socket_settings
from params.UserParams import *
import time

'''GLOBAL FUNCTION PARAMETERS'''
counter = 0


def flush_buffer(buffer_size):
    buffer = bytearray()
    for i in range(buffer_size):
        buffer.append(0)
    return buffer


def calculate_hibit(byte: int):
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


merge_dict = {}  # Create an empty byte for the merge function
for universes in range(socket_settings.universe_max + 1):  # It is as long as the highest possible universe.
    universe = calculate_hibit(universes)
    merge_dict[universe[0], universe[1]] = {}


def merge_sacn_inputs(sacn_data):  # Input Universe, CID and DMX data
    global merge_dict
    if sacn_data["cid"] not in merge_dict[sacn_data["universe"]]:
        merge_dict[sacn_data["universe"]].update({sacn_data["cid"]: {}})
        # Create new entry for this CID if not already created
    if "priority" not in merge_dict[sacn_data["universe"]][sacn_data["cid"]]:
        # If per channel priority does not exist yet, add it.
        per_channel_priority = bytearray()  # Create empty bytearray
        for i in range(512):
            per_channel_priority.append(sacn_data["priority"])  # Copy universe priority to every channel
        merge_dict[sacn_data["universe"]][sacn_data["cid"]].update(priority=per_channel_priority)
    merge_dict[sacn_data["universe"]][sacn_data["cid"]].update(dmx=sacn_data["dmx_data"], time=time.time())
    # Update Time and DMX data
    output_dmx = flush_buffer(512)  # Reset DMX output to 0
    output_priority = flush_buffer(512)  # Reset Priority output to 0
    for cids in merge_dict[sacn_data["universe"]]:  # Loop for every CID input on this universe
        for dmx_length in range(512):  # Loop for every position of the DMX packet
            if output_priority[dmx_length] < merge_dict[sacn_data["universe"]][cids]["priority"][dmx_length]:
                # If priority is higher, overwrite output.
                output_priority[dmx_length] = merge_dict[sacn_data["universe"]][cids]["priority"][dmx_length]
                if "dmx" not in merge_dict[sacn_data["universe"]][cids]:
                    pass
                else:
                    output_dmx[dmx_length] = merge_dict[sacn_data["universe"]][cids]["dmx"][dmx_length]
            if output_priority[dmx_length] == merge_dict[sacn_data["universe"]][cids]["priority"][dmx_length]:
                if "dmx" not in merge_dict[sacn_data["universe"]][cids]:
                    pass
                elif output_dmx[dmx_length] < merge_dict[sacn_data["universe"]][cids]["dmx"][dmx_length]:
                    # If priority is equal, the highest value wins.
                    output_dmx[dmx_length] = merge_dict[sacn_data["universe"]][cids]["dmx"][dmx_length]

    for universes in merge_dict:
        # If a universe has a timeout, remove it from the dictionary, so it won't overwrite the priority of the other
        # active universes.
        for cids in merge_dict[sacn_data["universe"]]:
            if time.time() - merge_dict[sacn_data["universe"]][cids]["time"] > E131_NETWORK_DATA_LOSS_TIMEOUT:
                if debug_level >= 2:
                    print(f"From {sacn_data['cid']} deleting universe {sacn_data['universe']} because of timeout after "
                          f"{time.time() - merge_dict[sacn_data['universe']][cids]['time']} seconds.")
                del merge_dict[sacn_data["universe"]][cids]
                # Delete the Universe on this CID and leave the loop.
                break

    sacn_data["dmx_data"] = output_dmx
    sacn_data["per_channel_priority"] = output_priority
    # Store these data in the input dict and return
    return sacn_data["dmx_data"]


def add_sacn_priority(sacn_data):
    global merge_dict
    if sacn_data["cid"] not in merge_dict[sacn_data["universe"]]:
        merge_dict[sacn_data["universe"]] = {sacn_data["cid"]: {}}
        # Create new entry for this CID if not already created
    per_channel_priority = bytearray()
    for i in range(512):
        per_channel_priority.append(sacn_data["per_channel_priority"][i])
    merge_dict[sacn_data["universe"]][sacn_data["cid"]].update(priority=per_channel_priority, time = time.time())


def identify_sacn_startcode(sacn_input):
    # Identifies the start code of this sACN packet
    if sacn_input[125] == 0x00:
        return "DMX"
    elif sacn_input[125] == 0xDD:
        return "PER_CHANNEL_PRIORITY"
    elif sacn_input[125] == 0xCC:
        return "RDM"
    else:
        return "ALTERNATE"


def identify_sacn_packet(sacn_input):
    # Identifies the type of this sACN packet. Raises an error if the packet is too short.
    try:
        len(sacn_input) < 126
        if len(sacn_input) < 126:
            raise TypeError("Unknown Package. The minimum length for a sACN package is 126.")
    except TypeError as error_message:
        if debug_level >= 1:
            print("LENGTH ERROR:", error_message)

    if tuple(sacn_input[40:44]) == VECTOR_E131_DATA_PACKET:  # sACN Data Packet
        return "sACN_DATA_PACKET"
    elif tuple(sacn_input[40:44]) == VECTOR_E131_EXTENDED_SYNCHRONIZATION:  # sACN Sync Packet
        return "sACN_EXTENDED_SYNCHRONIZATION"
    elif tuple(sacn_input[40:44]) == VECTOR_E131_EXTENDED_DISCOVERY:  # sACN Discovery Packet
        return "sACN_EXTENDED_DISCOVERY"


def sacn_data_check_validity(sacn_packet):
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

    # The following IF-Statements discard the package if it does not comply with E1.31 standards
    if tuple(sacn_packet[0:2]) != PREAMBLE_SIZE or tuple(sacn_packet[2:4]) != POST_AMBLE_SIZE or \
            tuple(sacn_packet[4:16]) != ACN_PACKET_IDENTIFIER or \
            tuple(sacn_packet[18:22]) != VECTOR_ROOT_E131_DATA or \
            tuple(sacn_packet[40:44]) != VECTOR_E131_DATA_PACKET or \
            sacn_packet[117] != VECTOR_DMP_SET_PROPERTY or \
            sacn_packet[118] != ADDRESS_TYPE_DATA_TYPE or \
            tuple(sacn_packet[119:121]) != FIRST_PROPERTY_ADDRESS or \
            tuple(sacn_packet[121:123]) != ADDRESS_INCREMENT:
        # Raise an error, if any of the package content is not valid. Print out what it should be and what was sent.
        raise TypeError(f"Package does not comply E1.31 standard! \
        Preamble {PREAMBLE_SIZE} was {tuple(sacn_packet[0:2])}, \
        Postamble {POST_AMBLE_SIZE} was {tuple(sacn_packet[2:4])}, \
        ACN Packet Identifier {ACN_PACKET_IDENTIFIER} was {tuple(sacn_packet[4:16])}, \
        VECTOR E1.31 {VECTOR_ROOT_E131_DATA} was {tuple(sacn_packet[18:22])}, \
        VECTOR E1.31 Data {VECTOR_ROOT_E131_DATA} was {tuple(sacn_packet[40:44])}, \
        VECTOR DMP {VECTOR_DMP_SET_PROPERTY} was {(sacn_packet[117])}, \
        Address Type {ADDRESS_TYPE_DATA_TYPE} was {sacn_packet[118]}, \
        First Property Address {FIRST_PROPERTY_ADDRESS} was {tuple(sacn_packet[119:121])}, \
        Address Increment {ADDRESS_INCREMENT} was {tuple(sacn_packet[121:123])}")


def sacn_dmx_input(sacn_packet):
    # If this is a normal DMX packet (Start Code = 0x00)
    # Dictionary with all the information we can get from this package
    sacn_data = {"cid": sacn_packet[22:38], "source_name": str(sacn_packet[44:108]), "priority": sacn_packet[108],
                 "sync_address": tuple(sacn_packet[109:111]), "sequence_number": sacn_packet[111],
                 "option_flags": sacn_packet[112], "universe": tuple(sacn_packet[113:115]),
                 "start_code": sacn_packet[125],
                 "dmx_data": sacn_packet[126:638], "universe_hibyte": sacn_packet[113],
                 "universe_lobyte": sacn_packet[114]}
    return sacn_data
    # Merge DMX data from multiple sources.


def sacn_per_channel_input(sacn_packet):
    # If this is a per channel priority packet (Start Code = 0xDD)
    # Dictionary with all the information we can get from this package
    sacn_data = {"cid": sacn_packet[22:38], "source_name": str(sacn_packet[44:108]),
                 "sync_address": tuple(sacn_packet[109:111]), "sequence_number": sacn_packet[111],
                 "option_flags": sacn_packet[112], "universe": tuple(sacn_packet[113:115]),
                 "start_code": sacn_packet[125],
                 "per_channel_priority": sacn_packet[126:638], "universe_hibyte": sacn_packet[113],
                 "universe_lobyte": sacn_packet[114]}
    return sacn_data


def sacn_rdm_input(sacn_packet):
    # If this is a alternate start code packet (Start Code != 0xDD or 0x00)
    # Dictionary with all the information we can get from this package
    sacn_data = {"cid": sacn_packet[22:38], "source_name": str(sacn_packet[44:108]), "priority": sacn_packet[108],
                 "sync_address": tuple(sacn_packet[109:111]), "sequence_number": sacn_packet[111],
                 "option_flags": sacn_packet[112], "universe": tuple(sacn_packet[113:115]),
                 "start_code": sacn_packet[125],
                 "alternate_data": sacn_packet[126:638], "universe_hibyte": sacn_packet[113],
                 "universe_lobyte": sacn_packet[114]}
    return sacn_data


def sacn_alternate_input(sacn_packet):
    pass


def sacn_sync_input(sacn_packet):
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
    # # # SYNCHRONIZATION PACKET FRAMING LAYER # # #
    # 38-39     Flags and lenght (Low 12 bits = PDU length, High 4 bits = 0x7
    # 40-43     Identifies 1.31 data as DMP Protocol PDU (VECTOR_E131_EXTENDED_SYNCHRONIZATION)
    # 44:       Sequence Number (To detect duplicate or out of order packets)
    # 45-46:    Synchronization Address (Universe on which synchronization packets are transmitted) <- Discard if zero
    # 47-48:    Reserved (Transmit as zero)

    # The following IF-Statement discards the package if it does not comply with E1.31 standards
    if tuple(sacn_packet[0:2]) != PREAMBLE_SIZE or tuple(sacn_packet[2:4]) != POST_AMBLE_SIZE or \
            tuple(sacn_packet[4:16]) != ACN_PACKET_IDENTIFIER or \
            tuple(sacn_packet[18:22]) != VECTOR_ROOT_E131_EXTENDED or \
            tuple(sacn_packet[40:44]) != VECTOR_E131_EXTENDED_SYNCHRONIZATION or \
            tuple(sacn_packet[45:47]) != (0, 0):
        # Raise an error, if any of the package content is not valid. Print out what it should be and what was sent.
        raise TypeError(f"Package does not comply E1.31 standard! \
        Preamble {PREAMBLE_SIZE} was {tuple(sacn_packet[0:2])}, \
        Postamble {POST_AMBLE_SIZE} was {tuple(sacn_packet[2:4])}, \
        ACN Packet Identifier {ACN_PACKET_IDENTIFIER} was {tuple(sacn_packet[4:16])}, \
        VECTOR E1.31 {VECTOR_ROOT_E131_EXTENDED} was {tuple(sacn_packet[18:22])}, \
        VECTOR E1.31 Sync {VECTOR_E131_EXTENDED_SYNCHRONIZATION} was {tuple[40:44]}")
    # Dictionary with all the information we can get from this package
    sACN_data = {"cid": sacn_packet[22:38], "sync_address": tuple(sacn_packet[45:47]),
                 "sequence_number": sacn_packet[44]}
    return sACN_data


def sacn_discovery_input(sacn_packet):
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
    # # # FRAMING LAYER # # #
    # 38-39     Flags and lenght (Low 12 bits = PDU length, High 4 bits = 0x7
    # 40-43     Identifies 1.31 data as DMP Protocol PDU (VECTOR_E131_EXTENDED_DISCOVERY)
    # 44-107:   Source Name assigned by User (UTF-8 encoded string)
    # 108-111:  Reserved (Transmit as zero)
    # # # UNIVERSE DISCOVERY LAYER # # #
    # 112-113:  Flags and length (Low 12 bits = PDU Length, High 4 bits = 0x7)
    # 114-117:  Identifies Universe Discovery data as universe list (VECTOR_UNIVERSE_DICOVERY_UNIVERSE_LIST)
    # 118:      Page (Indicating which packet of N this is - page numbers start at 0)
    # 119:      Final page (Page number N of the final page to be transmitted
    # 120-1143: List of Universes (Sorted list of up to 512 16-bit universes)

    # The following IF-Statement discards the package if it does not comply with E1.31 standards
    if tuple(sacn_packet[0:2]) != PREAMBLE_SIZE or tuple(sacn_packet[2:4]) != POST_AMBLE_SIZE or \
            tuple(sacn_packet[4:16]) != ACN_PACKET_IDENTIFIER or \
            tuple(sacn_packet[18:22]) != VECTOR_ROOT_E131_EXTENDED or \
            tuple(sacn_packet[40:44]) != VECTOR_E131_EXTENDED_DISCOVERY or \
            tuple(sacn_packet[114:118]) != VECTOR_UNIVERSE_DISCOVERY_UNIVERSE_LIST:
        # Raise an error, if any of the package content is not valid. Print out what it should be and what was sent.
        raise TypeError(f"Package does not comply E1.31 standard! \
        Preamble {PREAMBLE_SIZE} was {tuple(sacn_packet[0:2])}, \
        Postamble {POST_AMBLE_SIZE} was {tuple(sacn_packet[2:4])}, \
        ACN Packet Identifier {ACN_PACKET_IDENTIFIER} was {tuple(sacn_packet[4:16])}, \
        VECTOR E1.31 {VECTOR_ROOT_E131_EXTENDED} was {tuple(sacn_packet[18:22])}, \
        VECTOR E1.31 Discovery {VECTOR_E131_EXTENDED_DISCOVERY} was {tuple[40:44]}, \
        VECTOR E1.31 Discovery List {VECTOR_UNIVERSE_DISCOVERY_UNIVERSE_LIST} was {tuple[114:118]}")

    # Dictionary with all the information we can get from this package
    sACN_data = {"cid": sacn_packet[22:38], "source_name": str(sacn_packet[44:108]), "page": tuple(sacn_packet[118]),
                 "final_page": sacn_packet[119], "universes": sacn_packet[120:1143]}
    return sACN_data
