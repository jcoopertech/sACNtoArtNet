from load_settings import load_settings
from artnet.artnet_socket import artnet_broadcast_socket
from socket import timeout
from artnet.artnet_input import identify_artnet_packet, artnet_dmx_input
from artnet.artnet_socket import unicast_ips
from time import time
from sacn.sacn_output import sacn_dmx_output


def artnet_to_sacn():
    while True:
        try:
            input_packet, input_ip = artnet_broadcast_socket.recvfrom(1143)  # ToDo: Max Length
        except timeout:  # Ignore timeouts
            continue
        except BlockingIOError as Error:
            # print(Error, "Socket is blocked. Packets may get lost!")
            continue

        """Identify packets"""
        packet_type = identify_artnet_packet(input_packet)

        """DMX Type packet"""
        if packet_type == "DMX_PACKET":  # If it is a DMX startcode...
            if load_settings("artnet_to_sacn", "Art-Net") is True:  # ...and conversion is enabled...
                output = artnet_dmx_input(input_packet)   # ...read the DMX data, ...
                # output["dmx_data"] = merge_inputs(output)  # ... merge the inputs ...
                sacn_dmx_output(output)  # ... and send the packet.

            """ART_POLL"""
        elif packet_type == "ART_POLL":
            if input_ip not in unicast_ips:  # If receiver is new, add it to the receiver list
                unicast_ips[input_ip] = {"time": time()}
                print(f"Added {input_ip} to Art-Net receivers.")
            elif input_ip in unicast_ips:  # If it already exists, update timeout time
                unicast_ips[input_ip].update(time=time())
