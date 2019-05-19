from uuid import getnode as get_mac
import socket
import socket_settings
from ArtNetParams import *


def get_mac_ip():
    mac = hex(get_mac())
    return mac

def calculate_hibyte(byte: int):
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


def artpoll_output(target_ip="255.255.255.255", art_poll_reply=1, diagnostics=0, unicast=1, vlc=1, priority=DP_LOW):
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpOutput, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        TalkToMe
    #           0:Deprecated,
    #           1: Send ArtPollReply whenever Node conditions change. This selection allows the controller to be
    #           informed of changes without of the need of continuously poll.
    #           2: 1 = Send diagnostic messages, 0 = Do not send diagnostic messages
    #           3: 1 = Diagnostics are unicast, 0 = Diagnostics are unicast (dependent of bit 2)
    #           4: 1 = Disable VLC transmission, 0 = Enable VLC transmission
    #           5-7: Unused, transmit as zero, do not test upon receipt
    # 6:        Priority (The lowest priority of diagnostics message that should be sent)

    talk_to_me = int(f"000{vlc}{unicast}{diagnostics}{art_poll_reply}0",2)  # Flags, Bit 0 and 5-7 unused

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_POLL[1])  # OPCode Lo
    artnet_packet.append(OP_POLL[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(talk_to_me)   # TalkToMe
    artnet_packet.append(priority)  # Priority

    try:
        socket_settings.set_artnet_sock.sendto(artnet_packet, (target_ip, UDP_PORT))
        print(f"Sending {artnet_packet} to {target_ip}")
    except Exception as exception:
        print(f"Socket error: {exception}")


def artpollreply_output(target_ip='255.255.255.255', universe=0, ubea_version=0, indicator_state=00,
                        programming_authority=00, firmware_boot=0, rdm_capable=0, ubea_present=0,
                        esta_manufacturer=0x0000, short_name="The Converter", long_name="sACN to Art-Net Converter",
                        node_report="0", num_ports=0, artnet_output=[0,0,0,0], artnet_input=[0,0,0,0], protocol="Art-Net",
                        input_received=0, input_test_packet=0, input_sip=0, input_text=0, input_disabled=0,
                        input_error=0, output_received=0, output_test_packet=0, output_sip=0, output_text=0,
                        output_merging=0, output_short=0, output_ltp=0, output_sacn=1, m1=0, m2=0, m3=0, m4=0, m5=0,
                        m6=0, m7=0, m8=0, r1=0, r2=0, r3=0, r4=0, r5=0, r6=0, r7=0, r8=0, style_code=ST_ROUTE,
                        bind_index=1, web_browser_config=0, dhcp=0, dhcp_capable=0, bit_support15=1, switch_to_sacn=1,
                        squawking=0):
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpPollReply, see OPCode list) -> Int16!
    # 3:        IP Address[4] (Node's IP address. First array entry is most significant byte of address
    # 4:        Port (0x1936). Low byte first
    # 5:        VersInfoH (High Byte of Nodes firmware revision. Controller should use this field to decide if a
    # 6:        VersInfoL firmware update should proceed. Convention: Higher number = More recent release.)
    # 7:        NetSwitch (Bits 14-8 of the 15 bit Port address are encoded into the bottom 7 bits of this field.
    #          This is used in combination with Subswitch and SwIn[] or SwOut[] th produce the full input_data address.)
    # 8:        SubSwitch (Bits 7-4 of the 15 bit Port address are encoded into the bottom 7 bits of this field.)
    # 9:        OemHi (High byte of the Oem value)
    # 10:       OemLo (Low byte of the Oem value. Current OEM Codes in file Oem_Codes.py)
    # 11:       Ubea Version (User Bios Extension Area. If the UBEA is not programmed, this field contains zero.)
    # 12:       Status1
    #           0: 1 = UBEA present, 0 = UBEA not present
    #           1: 1 = Capable of RDM, 0 = Not capable of RDM
    #           2: 1 = Booted from ROM, 0 = Booted from flash. Nodes that don't support dual boot, send zero.
    #           3: Not implemented, transmit as zero, receivers do not test
    #           4-5: Address Programming Authority
    #               00 = Port Address Programming Authority unknown
    #               01 = All Port-Address set by front panel controls
    #               10 = All or part of Port-Address programmed by network or web browser
    #               11 = Not used
    #           6-7: Indicator state
    #               00 = Indicator State unknown
    #               01 = Indicators in Locate/Identify mode
    #               10 = Indicators in Mute Mode
    #               11 = Indicators in Normal Mode
    # 13:       EstaManLo (The ESTA Manufacturer code. Assigned by ESTA)
    # 14:       EstaManHi
    # 15:       ShortName (Null terminated short name for the node. Controller uses ArtAddress to program this string.
    #           Max length is 17 characters plus the null.)
    # 16:       Long Name (Null terminated long name for the node. Controller uses ArtAddress to program this string.
    #           Max length is 63 character plus the null.)
    # 17:       NodeReport: Textual report of the Node's operating status or operational errors. Primarily intended for
    #           engineering data, not end user data. Format: "#xxxx [yyyy..] zzzz..."
    #               xxxx = hex status node report code (See variables above)
    #               yyyy = decimal counter that increments every time the Node sends an ArtPollResponse.
    #                      This allows monitoring of event changes in the node.
    #               zzzz = English text sting defining the status.
    # 18:       NumPortsHi (For future expansion and is currently zero)
    # 19:       NumPortsLo (Number of input and output ports. Transmit zero if no inputs and outputs are implemented.
    #           Maximum value is 4. Nodes can ignore this field.
    # 20:       PortTypes[4]: This array defines the operation and protocol of each channel.
    #           (4 inputs + 4 ouputs = 0xc0, 0x0c, 0x0c, 0x0c)
    #               0-5: 000000 = DMX512, 000001 = MIDI, 000010 = Avab,
    #                    000011 = Colortran CMX, 000100 = ADB 62.5, 000101 = Art-Net
    #               6: Set if this channel can input onto the Art-Net Network
    #               7: Set if this channel can output data from the Art-Net Network
    # 21:       GoodInput[4] (defines input status of the node)
    #               0-1: Unused and transmitted as zero
    #               2: 1 = Receive errors detected
    #               3: 1 = Input is disabled
    #               4: 1 = Channel includes DMX512 text packets
    #               5: 1 = Channel includes DMX512 SIPs
    #               6: 1 = Channel includes DMX512 test packets
    #               7: 1 = Data received
    # 22:       GoodOutput[4] (defines output status if the node)
    #               0: 1 = Output selected to transmit sACN, 0 = Output selected to transmit Art-Net
    #               1: 1 = Merge Mode is LTP, 0 = Merge Mode is HTP
    #               2: 1 = DMX output short detected on power up
    #               3: 1 = Output is merging ArtNet data
    #               4: 1 = Channel includes DMX512 text packets
    #               5: 1 = Channel includes DMX512 SIPs
    #               6: 1 = Channel includes DMX512 test packets
    #               7: 1 = Data is being transmitted
    # 23:      SwIn[4] (Bits 0-3 of the 15 bit Port address for each of the 4 possible inputs are encoded in low 4 bits)
    # 24:     SwOut[4] (Bits 0-3 of the 15 bit Port address for each of the 4 possible inputs are encoded in low 4 bits)
    # 25:       SwVideo (Deprecated)
    # 26:       SwMacro (0 = Macro 1 active ... 7 = Macro 8 active)
    # 27:       SwRemote (0 = Remote 1 active ... 7 = Remote 8 active)
    # 28-30:    Spare (0x0, 0x0, 0x0)
    # 31:       Style (Equipment style of the device. See table above)
    # 32:       MAC Hi (Mac Address Hi Byte. Set to zero if node canot supply this information, aa)
    # 33-36:    MAC (MAC Address bb-cc-dd-ee)
    # 37:       MAC Lo (MAC Address Lo Byte, ff)
    # 38:       BindIP[4] (IP of the root device if the device is larger or modular)
    # 39:       BindIndex (Order of bound devices. 1 = root device)
    # 40:       Status 2:
    #               0: 1 = Product supports web browser configuration
    #               1: 1 = Node's IP is DHCP configured, 0 = Node's IP is manually configured
    #               2: 1 = Node is DHCP capable, 0 = Node is not DHCP capable
    #              3: 1 = Node supports 15bit Port Address (Art-Net 3+), 0 = Node supports 8 bit Port Addr. (Art-Net 2)
    #               4: 1 = Node able to switch between Art-Net and sACN, 0 = Not able to switch
    #               5: 1 = Squawking, 0 = Not squawking
    # 41:       Transmit as zero (26x8!!!)

    port = calculate_hibyte(UDP_PORT)
    ip = socket.gethostbyname(socket.gethostname())
    ip = ip.split(".")
    vers_info = calculate_hibyte(VERSION)
    net_switch = calculate_hibyte(universe)
    oem = calculate_hibyte(OEM_CODE)
    status1 = int(f"{indicator_state}{programming_authority}0{firmware_boot}{rdm_capable}{ubea_present}", 2)
    esta_manufacturer = calculate_hibyte(esta_manufacturer)
    short = bytearray(short_name.ljust(17)[:17], "UTF_8")
    long = bytearray(long_name.ljust(63)[:63], "UTF_8")
    node = bytearray(node_report.ljust(64)[:64], "UTF_8")
    if protocol == "DMX512":
        protocol_flag = 000000
    elif protocol == "MIDI":
        protocol_flag = "000001"
    elif protocol == "Avab":
        protocol_flag = "000010"
    elif protocol == "Colortran CMX":
        protocol_flag = "000011"
    elif protocol == "ADB 62.5":
        protocol_flag = "000100"
    elif protocol == "Art-Net":
        protocol_flag = "000101"
    port1 = int(f"{artnet_output[0]}{artnet_input[0]}{protocol_flag}", 2)
    port2 = int(f"{artnet_output[1]}{artnet_input[1]}{protocol_flag}", 2)
    port3 = int(f"{artnet_output[2]}{artnet_input[2]}{protocol_flag}", 2)
    port4 = int(f"{artnet_output[3]}{artnet_input[3]}{protocol_flag}", 2)
    good_input = int(f"{input_received}{input_test_packet}{input_sip}{input_text}{input_disabled}{input_error}00", 2)
    good_output = int(f"{output_received}{output_test_packet}{output_sip}{output_text}{output_merging}{output_short}{output_ltp}{output_sacn}", 2)
    good_input1 = good_input
    good_input2 = good_input
    good_input3 = good_input
    good_input4 = good_input
    good_output1 = good_output
    good_output2 = good_output
    good_output3 = good_output
    good_output4 = good_output
    universe1 = universe
    universe2 = universe
    universe3 = universe
    universe4 = universe
    macro = int(f"{m8}{m7}{m6}{m5}{m4}{m3}{m2}{m1}", 2)
    remote = int(f"{r8}{r7}{r6}{r5}{r4}{r3}{r2}{r1}", 2)
    mac = get_mac_ip()
    mac_u = int(mac[2:4], 16)
    mac_v = int(mac[4:6], 16)
    mac_w = int(mac[6:8], 16)
    mac_x = int(mac[8:10], 16)
    mac_y = int(mac[10:12], 16)
    mac_z = int(mac[12:14], 16)
    print(mac)
    print(mac_u)
    status2 = int(f"000{squawking}{switch_to_sacn}{bit_support15}{dhcp_capable}{dhcp}{web_browser_config}", 2)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_POLL_REPLY[1])  # OPCode Lo
    artnet_packet.append(OP_POLL_REPLY[0])  # OPCode Hi
    artnet_packet.append(int(ip[0]))    # IP A
    artnet_packet.append(int(ip[1]))    # IP B
    artnet_packet.append(int(ip[2]))    # IP C
    artnet_packet.append(int(ip[3]))    # IP D
    artnet_packet.append(port[1])  # Port Lo
    artnet_packet.append(port[0])  # Port Hi
    artnet_packet.append(vers_info[0])  # VersInfo Hi
    artnet_packet.append(vers_info[1])  # VersInfo Lo
    artnet_packet.append(net_switch[1])  # Net Switch Lo <- To Do
    artnet_packet.append(net_switch[0])  # Net Switch Hi
    artnet_packet.append(oem[0])    # OEM Hi
    artnet_packet.append(oem[1])    # OEM Lo
    artnet_packet.append(ubea_version)  # ubea
    artnet_packet.append(status1)   # status1
    artnet_packet.append(esta_manufacturer[1])  # ESTA Lo
    artnet_packet.append(esta_manufacturer[0])  # Esta Hi
    artnet_packet.extend(short)    # short (17 char+null) <- To Do
    artnet_packet.append(0x0)
    artnet_packet.extend(long)     # long (63 char+null) <- To Do
    artnet_packet.append(0x0)
    artnet_packet.extend(node)   # report (64 char) <- To Do
    artnet_packet.append(0x0)  # NumPorts Hi
    artnet_packet.append(num_ports)  # NumPorts Lo
    artnet_packet.append(port1)
    artnet_packet.append(port2)
    artnet_packet.append(port3)
    artnet_packet.append(port4)
    artnet_packet.append(good_input1)
    artnet_packet.append(good_input2)
    artnet_packet.append(good_input3)
    artnet_packet.append(good_input4)
    artnet_packet.append(good_output1)
    artnet_packet.append(good_output2)
    artnet_packet.append(good_output3)
    artnet_packet.append(good_output4)
    artnet_packet.append(universe1)  # SwIn1
    artnet_packet.append(universe2)  # SwIn2
    artnet_packet.append(universe3)  # SwIn3
    artnet_packet.append(universe4)  # SwIn4
    artnet_packet.append(universe1)  # SwOut1
    artnet_packet.append(universe2)  # SwOut2
    artnet_packet.append(universe3)  # SwOut3
    artnet_packet.append(universe4)  # SwOut4
    artnet_packet.append(0x0)  # SwVideo (deprecated)
    artnet_packet.append(macro)
    artnet_packet.append(remote)
    artnet_packet.append(SPARE)
    artnet_packet.append(SPARE)
    artnet_packet.append(SPARE)
    artnet_packet.append(style_code)
    artnet_packet.append(mac_u)    # MAC Hi
    artnet_packet.append(mac_v)
    artnet_packet.append(mac_w)
    artnet_packet.append(mac_x)
    artnet_packet.append(mac_y)
    artnet_packet.append(mac_z)    # MAC Lo
    artnet_packet.append(int(ip[0]))  # Bind IP A
    artnet_packet.append(int(ip[1]))  # Bind IP B
    artnet_packet.append(int(ip[2]))  # Bind IP C
    artnet_packet.append(int(ip[3]))  # Bind IP D
    artnet_packet.append(bind_index)
    artnet_packet.append(status2)
    for x in range(0, 27):
        artnet_packet.append(0x0)  # Filler

    try:
        socket_settings.set_artnet_sock.sendto(artnet_packet, (target_ip, UDP_PORT))
        print(f"Sending {artnet_packet} to {target_ip}")
    except Exception as exception:
        print(f"Socket error: {exception}")


def artdmx_output(artnet_data, target_ip="255.255.255.255", fps=30, physical=0):
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpOutput, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Sequence (increment in the range 0x01 to 0xff. Set to 0x00 to disable the feature)
    # 6:        Physical (Phyiscal Input Port, information for the user only)
    # 7:        SubUni (Low Byte of the 15 bit Port-Address to which this packet is destined)
    # 8:        Net (Top 7 bits of the 15 bit Port-Address to which this packet is destined)
    # 9:        LengthHi (Length of the DMX512 data array. Should be between 2 and 512)
    # 10:       Lenght (Low Byte of above)
    # 11:       DMX512 data array

    length = calculate_hibyte(512)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_DMX[1])  # OPCode Lo
    artnet_packet.append(OP_DMX[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(artnet_data["sequence_number"])  # Sequence <- To Do
    artnet_packet.append(physical)  # Physical
    artnet_packet.append(artnet_data["universe_lobyte"])  # SubUni
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(length[0])  # LengthHi
    artnet_packet.append(length[1])  # Length
    artnet_packet.extend(bytearray(artnet_data["dmx_data"]))

    try:
        socket_settings.set_artnet_sock.sendto(artnet_packet, (target_ip, UDP_PORT))
        #print(f"Sending {artnet_packet} to {target_ip}")
    except Exception as exception:
        print(f"Socket error: {exception}")


def identify_artnet_packet(input):
    # Extracts the type of ArtNet packet and will return the type of packet and the packet itself.
    if len(input) < 1:
        raise TypeError("Unknown Package. The minimum length for a sACN package is ...") #<- To Do
    if input[8] == OP_DMX[1] and input[9] == OP_DMX[0]:
        print("DMX PACKET")
    elif input[8] == OP_POLL[1] and input[9] == OP_POLL[0]:
        print("ART POLL")
        artpollreply_output(PRIMARY_ARTNET_ADDRESS,)
    elif input[8] == OP_POLL_REPLY[1]and input[9] == OP_POLL_REPLY[0]:
        print("ART POLL REPLY")