from load_settings import load_settings
from sacn.sacn_socket import sacn_socket
from socket import timeout
from sacn.sacn_input import identify_packet, identify_startcode, sacn_dmx_input, sacn_per_channel_input, merge_inputs, \
    add_per_channel_priority
from artnet.artnet_output import artdmx_output


def sacn_to_artnet():
    """sACN to Art-Net"""
    while True:
        if load_settings("sacn_to_artnet", "sACN") is True:
            try:
                input_packet, input_ip = sacn_socket.recvfrom(1143)  # 1143 is the max length for a sACN packet
            except timeout:  # Ignore timeouts
                continue

            """Identify packets"""
            packet_type = identify_packet(input_packet)

            """Data Type Packet"""
            if packet_type == "sACN_DATA_PACKET":
                startcode = identify_startcode(input_packet)
                if startcode == "DMX":  # If it is a DMX startcode...
                    output = sacn_dmx_input(input_packet)  # ... read the DMX data, ...
                    output["dmx_data"] = merge_inputs(output)  # ... merge the inputs...
                    artdmx_output(output)  # ... and send the packet.
                elif startcode == "PER_CHANNEL_PRIORITY":  # If it is a DMX startcode...
                    output = sacn_per_channel_input(input_packet)  # ... read the priority data...
                    add_per_channel_priority(output)  # ... and add the per channel priority to the merge input_dict.
                elif startcode == "RDM":
                    print("RDMNet packet")
                    pass  # <- ToDo
                elif identify_startcode(packet_type) == "ALTERNATE":
                    print("Unknown start code")
                    pass  # <- ToDo
                else:
                    print("Unknown package")
                    pass

                """Synchronisation Type Packet"""
            elif packet_type == "sACN_EXTENDED_SYNCHRONISATION":
                print("Extended Sync Packet")
                pass  # <- ToDo
            elif packet_type == "sACN_EXTENDED_DISCOVERY":
                print("Extended Discovery Packet")
                pass  # <- ToDo
            else:
                pass
