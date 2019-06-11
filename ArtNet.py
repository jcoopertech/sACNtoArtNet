from uuid import getnode as get_mac
import socket
import socket_settings
from params.ArtNetParams import *
from params.RDMParams import *


set_artnet_sock = socket_settings.artnet_socket_setup(socket_settings.ip)


def get_mac_ip():
    mac = hex(get_mac())  # Using the UUID Lib to read the device IP
    return mac


def calculate_hibyte(byte: int): # Returns a list with the hibyte[0] and the lobyte[1]
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


def artpoll_output(target_ip="255.255.255.255", art_poll_reply=1, diagnostics=0, unicast=1, vlc=1, priority=DP_LOW):
    # BROADCAST
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

    talk_to_me = int(f"000{vlc}{unicast}{diagnostics}{art_poll_reply}0", 2)  # Flags, Bit 0 and 5-7 unused

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_POLL[1])  # OPCode Lo
    artnet_packet.append(OP_POLL[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(talk_to_me)   # TalkToMe
    artnet_packet.append(priority)  # Priority

    artnet_output(artnet_packet, target_ip)


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
    # BROADCAST
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
    artnet_packet.append(net_switch[1])  # Net Switch Lo <- ToDo
    artnet_packet.append(net_switch[0])  # Net Switch Hi
    artnet_packet.append(oem[0])    # OEM Hi
    artnet_packet.append(oem[1])    # OEM Lo
    artnet_packet.append(ubea_version)  # ubea
    artnet_packet.append(status1)   # status1
    artnet_packet.append(esta_manufacturer[1])  # ESTA Lo
    artnet_packet.append(esta_manufacturer[0])  # Esta Hi
    artnet_packet.extend(short)    # short (17 char+null) <- ToDo
    artnet_packet.append(0x0)
    artnet_packet.extend(long)     # long (63 char+null) <- ToDo
    artnet_packet.append(0x0)
    artnet_packet.extend(node)   # report (64 char) <- ToDo
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

    artnet_output(artnet_packet, target_ip)


def artdmx_output(artnet_data, target_ip="255.255.255.255", fps=30, physical=0):
    # 0-39 DEVICES: UNICAST, 40+ DEVICES: BROADCAST
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
    artnet_packet.append(artnet_data["sequence_number"])  # Sequence <- ToDo
    artnet_packet.append(physical)  # Physical
    artnet_packet.append(artnet_data["universe_lobyte"])  # SubUni
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(length[0])  # LengthHi
    artnet_packet.append(length[1])  # Length
    artnet_packet.extend(bytearray(artnet_data["dmx_data"]))

    artnet_output(artnet_packet, target_ip)


def artipprog_output(target_ip="255.255.255.255", any_programming=0, dhcp_enable=0, default_reset=0,
                     program_ip=0, program_subnet=0, prog_ip="127.0.0.1", prog_sm="255.0.0.0"):
    # UNICAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpIpProg, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Pad length to match ArtPoll)
    # 6:        Filler 2 (Pad length to match ArtPoll)
    # 7:        Command (If all zero, it is an inquiry only)
    #           0: Program Port (Deprecated)
    #           1: Program Subnet Mask
    #           2: Program IP address
    #           3: Set all three parameters to default
    #           4-5: Not used, transit as zero)
    #           6: Enable DHCP (ignore bits 0-5 if set to 1)
    #           7: Set to enable any programming
    # 8:        Filler 4 (Set to zero)
    # 9:        ProgIpHi (IP Address to be programmed into Node if enabled by Command Field)
    # 10:       ProgIp2 (BBB)
    # 11:       ProgIp1 (CCC)
    # 12:       ProgIpLo (DDD)
    # 13:       ProgSmHi (Subnet Mask to be programmed into Node if enabled by Command Field)
    # 14:       ProgSm2 (BBB)
    # 15:       ProgSm1 (CCC)
    # 16:       ProgSmLo (DDD)
    # 17:       ProgPortHi (Deprecated)
    # 18:       ProgPortLo (Deprecated)
    # 19-26:    Spare 1-8 (Transmit as zero, receivers don't test)

    command = int(f"{any_programming}{dhcp_enable}00{default_reset}{program_ip}{program_subnet}0", 2)
    prog_ip = list(map(int, prog_ip.split(".")))
    prog_sm = list(map(int, prog_sm.split(".")))

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_IP_PROG[1])     # OPCode Lo
    artnet_packet.append(OP_IP_PROG[0])     # OPCode Hi
    artnet_packet.append(PROT_VER_HI)       # ProtVerHi
    artnet_packet.append(PROT_VER_LO)       # ProtVerLo
    artnet_packet.append(0x00)              # Filler 1
    artnet_packet.append(0x00)              # Filler 2
    artnet_packet.append(command)           # Command
    artnet_packet.append(0x00)              # Filler 4
    artnet_packet.append(prog_ip[0])        # Prog IP Hi
    artnet_packet.append(prog_ip[1])
    artnet_packet.append(prog_ip[2])
    artnet_packet.append(prog_ip[3])        # Prog IP Lo
    artnet_packet.append(prog_sm[0])        # Prog Sm Hi
    artnet_packet.append(prog_sm[1])
    artnet_packet.append(prog_sm[2])
    artnet_packet.append(prog_sm[3])        # Prog Sm Lo
    artnet_packet.append(0x00)              # Prog Port Hi (Deprecated)
    artnet_packet.append(0x00)              # Prog Port Lo (Deprecated)
    for i in range(8):
        artnet_packet.append(0x00)          # Spare 1-8

    artnet_output(artnet_packet, target_ip)


def artipprogreply_output(target_ip="255.255.255.255", dhcp_enable=0, prog_ip="127.0.0.1", prog_sm="255.0.0.0"):
    # UNICAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpIpProgReply, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Pad length to match ArtPoll)
    # 6:        Filler 2 (Pad length to match ArtPoll)
    # 7:        Filler 3 (Pad length to match ArtIpProg)
    # 8:        Filler 4 (Pad length to match ArtIpProg)
    # 9:        ProgIpHi (IP Address to be programmed into Node if enabled by Command Field)
    # 10:       ProgIp2 (BBB)
    # 11:       ProgIp1 (CCC)
    # 12:       ProgIpLo (DDD)
    # 13:       ProgSmHi (Subnet Mask to be programmed into Node if enabled by Command Field)
    # 14:       ProgSm2 (BBB)
    # 15:       ProgSm1 (CCC)
    # 16:       ProgSmLo (DDD)
    # 17:       ProgPortHi (Deprecated)
    # 18:       ProgPortLo (Deprecated)
    # 19:       Status
    #           0-5: 0
    #           6: DHCP Enabled
    #           7: 0
    # 20-26:    Spare 2-8 (Transmit as zero, receivers don't test)

    prog_ip = list(map(int, prog_ip.split(".")))
    prog_sm = list(map(int, prog_sm.split(".")))
    command = int(f"0{dhcp_enable}000000", 2)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_IP_PROG_REPLY[1])  # OPCode Lo
    artnet_packet.append(OP_IP_PROG_REPLY[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x00)  # Filler 1
    artnet_packet.append(0x00)  # Filler 2
    artnet_packet.append(0x00)  # Filler 3
    artnet_packet.append(0x00)  # Filler 4
    artnet_packet.append(prog_ip[0])  # Prog IP Hi
    artnet_packet.append(prog_ip[1])
    artnet_packet.append(prog_ip[2])
    artnet_packet.append(prog_ip[3])  # Prog IP Lo
    artnet_packet.append(prog_sm[0])  # Prog Sm Hi
    artnet_packet.append(prog_sm[1])
    artnet_packet.append(prog_sm[2])
    artnet_packet.append(prog_sm[3])  # Prog Sm Lo
    artnet_packet.append(0x00)  # Prog Port Hi (Deprecated)
    artnet_packet.append(0x00)  # Prog Port Lo (Deprecated)
    artnet_packet.append(command)
    for i in range(7):
        artnet_packet.append(0x00)  # Spare 2-8

    artnet_output(artnet_packet, target_ip)


def artaddress_output(target_ip='255.255.255.255', net_switch=0x7f, bind_index=1, short_name="The Converter",
                      long_name="sACN to Art-Net Converter", sw_in1=0x7f, sw_in2=0x7f, sw_in3=0x7f, sw_in4=0x7f,
                      sw_out1=0x7f, sw_out2=0x7f, sw_out3=0x7f, sw_out4=0x7f, sub_switch=0x7f, command=0x00):
    # UNICAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpAddress, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        NetSwitch (Bits 14-8 of the 15 bit Port address are encoded into the bottom 7 bits of this field.
    #          This is used in combination with Subswitch and SwIn[] or SwOut[] th produce the full input_data address.
    #          Value is ignored unless bit 7 is high -> to send 0x07, send 0x87. 0x00 = Reset to physical switch
    #          setting, 0x7f = No change)
    # 6:        Bind Index (Defines the bound node which originated this packet and is used to uniquely identify the
    #           bound node when Identical IP addresses are in use. Represents the order of bound devices
    #           A lower number means closer to the root device. 1 = Root Device
    # 7:        ShortName (Null terminated short name for the node. Controller uses ArtAddress to program this string.
    #           Max length is 17 characters plus the null.)
    # 8:        Long Name (Null terminated long name for the node. Controller uses ArtAddress to program this string.
    #           Max length is 63 character plus the null.)
    # 9:        SwIn[4] (Bits 0-3 of the 15 bit Port address for each of the 4 possible inputs are encoded in low 4
    #           bits. Value is ignored unless bit 7 is high. 0x00 = Reset to physical switch setting, 0x7f = No change)
    # 10:       SwOut[4] (Bits 0-3 of the 15 bit Port address for each of the 4 possible inputs are encoded in low 4
    #           bits. Value is ignored unless bit 7 is high. 0x00 = Reset to physical switch setting, 0x7f = No change)
    # 11:       SubSwitch (Bits 7-4 of the 15 bit Port address are encoded into the bottom 7 bits of this field.
    #           Value is ignored unless bit 7 is high. 0x00 = Reset to physical switch setting, 0x7f = No change)
    # 12:       SwVideo (Deprecated)
    # 13:       Command
    #           0x00: AcNone (No action)
    #           0x01: AcCancelMerge (If node is in merge mode, cancel merge upon receive of next ArtDmx packet
    #           0x02: AcLedNormal (The front panel leds operate normally
    #           0x03: AcLedMute (The front panel leds are disabled and switched off
    #           0x04: AcLedLocate (Rapid flashing for identification)
    #           0x05: AcResetRx Flags (Resets the node's Sip, Text, Text and data error flags
    #           0x10: AcMergeLtp0 (Set DMX Port 0 to Merge in LTP mode
    #           0x11: AcMergeLtp1 (Set DMX Port 1 to Merge in LTP mode
    #           0x12: AcMergeLtp2 (Set DMX Port 2 to Merge in LTP mode
    #           0x13: AcMergeLtp3 (Set DMX Port 3 to Merge in LTP mode
    #           0x50: AcMergeHtp0 (Set DMX Port 0 to Merge in HTP mode
    #           0x51: AcMergeHtp1 (Set DMX Port 1 to Merge in HTP mode
    #           0x52: AcMergeHtp2 (Set DMX Port 2 to Merge in HTP mode
    #           0x53: AcMergeHtp3 (Set DMX Port 3 to Merge in HTP mode
    #           0x60: AcArtNetSel0 (Set DMX Port 0 to output RDM and DMX from Art-Net protocol)
    #           0x61: AcArtNetSel1 (Set DMX Port 1 to output RDM and DMX from Art-Net protocol)
    #           0x62: AcArtNetSel2 (Set DMX Port 2 to output RDM and DMX from Art-Net protocol)
    #           0x63: AcArtNetSel3 (Set DMX Port 3 to output RDM and DMX from Art-Net protocol)
    #           0x70: AcAcnSel0 (Set DMX Port 0 to output RDM from Art-Net protocol and DMX from sACN protocol)
    #           0x71: AcAcnSel1 (Set DMX Port 1 to output RDM from Art-Net protocol and DMX from sACN protocol)
    #           0x72: AcAcnSel2 (Set DMX Port 2 to output RDM from Art-Net protocol and DMX from sACN protocol)
    #           0x73: AcAcnSel3 (Set DMX Port 3 to output RDM from Art-Net protocol and DMX from sACN protocol)
    #           0x90: AcClearOp0 (Clear DMX output buffer for Port 0)
    #           0x91: AcClearOp1 (Clear DMX output buffer for Port 1)
    #           0x92: AcClearOp2 (Clear DMX output buffer for Port 2)
    #           0x93: AcClearOp3 (Clear DMX output buffer for Port 3)

    short = bytearray(short_name.ljust(17)[:17], "UTF_8")
    long = bytearray(long_name.ljust(63)[:63], "UTF_8")

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_ADDRESS[1])  # OPCode Lo
    artnet_packet.append(OP_ADDRESS[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(net_switch)  # Net Switch Lo <- ToDo
    artnet_packet.append(bind_index)    # Bind Index
    artnet_packet.extend(short)  # short (17 char+null) <- ToDo
    artnet_packet.append(0x0)
    artnet_packet.extend(long)  # long (63 char+null) <- ToDo
    artnet_packet.append(0x0)
    artnet_packet.append(sw_in1)  # SwIn1
    artnet_packet.append(sw_in2)  # SwIn2
    artnet_packet.append(sw_in3)  # SwIn3
    artnet_packet.append(sw_in4)  # SwIn4
    artnet_packet.append(sw_out1)  # SwOut1
    artnet_packet.append(sw_out2)  # SwOut2
    artnet_packet.append(sw_out3)  # SwOut3
    artnet_packet.append(sw_out4)  # SwOut4
    artnet_packet.append(sub_switch)  # Subswitch
    artnet_packet.append(0x00)       # SwVideo
    artnet_packet.append(command)

    artnet_output(artnet_packet, target_ip)


def artdiagdata_output(target_ip="255.255.255.255", priority=DP_LOW, data="Everything is ok"):
    # UNICAST or BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpDiagData, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Priority (See Priority Code List)
    # 7:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 8:        Filler 3 (Ignore by receivers, set to zero by sender.)
    # 9:        LengthHi (Length of the text array below)
    # 10:       LengthLo
    # 11:       Data (ASCII Text array, null terminated. Max length is 512 bytes including the null terminator)

    if len(data) > 511:
        data = data[0:511]
    data_length = calculate_hibyte(len(data)+1)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_DIAG_DATA[1])  # OPCode Lo
    artnet_packet.append(OP_DIAG_DATA[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x00)  # Filler 1
    artnet_packet.append(priority)  # Priority
    artnet_packet.append(0x00)  # Filler 2
    artnet_packet.append(0x00)  # Filler 3
    artnet_packet.append(data_length[1])
    artnet_packet.append(data_length[0])
    artnet_packet.extend(data)  # Data
    artnet_packet.append(0x00)  # Null termination

    artnet_output(artnet_packet, target_ip)


def arttimecode_output(target_ip="255.255.255.255", frames=0, seconds=0, minutes=0, hours=0, frame_type="SMPTE"):
    # UNICAST or BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpTimeCode, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        Frames (Frames time. 0-29 depending on mode)
    # 8:        Seconds (0-59)
    # 9:        Minutes (0-59)
    # 10:       Hours (0-23)
    # 11:       Type
    #           0: Film (24FPS)
    #           1: EBU (25FPS)
    #           2: DF (29,97FPS)
    #           3: SMPTE (30FPS)

    if frame_type == "Film":
        frame_type = 0
    elif frame_type == "EBU":
        frame_type = 1
    elif frame_type == "DF":
        frame_type = 2
    elif frame_type == "SMTPE":
        frame_type = 3

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_TIME_CODE[1])  # OPCode Lo
    artnet_packet.append(OP_TIME_CODE[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x00)  # Filler 1
    artnet_packet.append(0x00)  # Filler 2
    artnet_packet.append(frames)  # Frames
    artnet_packet.append(seconds)
    artnet_packet.append(minutes)
    artnet_packet.append(hours)
    artnet_packet.append(frame_type)  # Frame Type

    artnet_output(artnet_packet, target_ip)


def artcommand_output(target_ip="255.255.255.255", esta_code=0xFFFF, art_command=SW_OUT_TEXT):
    # UNICAST or BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpArtCommand, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        EstaManHi (ESTA Manufacturer Code. See ESTA Code list)
    # 6:        EstaManLo (Lo byte of above (???))
    # 7:        LengthHi (Length of the text array below)
    # 8:        LengthLo
    # 9:        Data (ASCII Text array, null terminated. Max length is 512 bytes including the null terminator)
    #           See Command Code List

    esta_code = calculate_hibyte(esta_code)
    if len(art_command) > 511:
        art_command = art_command[0:511]
    data_length = calculate_hibyte(len(art_command) + 1)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_COMMAND[1])  # OPCode Lo
    artnet_packet.append(OP_COMMAND[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(esta_code[1])  # EstaManHi
    artnet_packet.append(esta_code[0])  # EstaManLo
    artnet_packet.append(data_length[1])  # Length Hi
    artnet_packet.append(data_length[0])   # Length Lo
    artnet_packet.extend(art_command)   # Art Command

    artnet_output(artnet_packet, target_ip)


def arttrigger_output(target_ip="255.255.255.255", oem_code=0xFFFF, key=255, subkey=0, data=""):
    # UNICAST or BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpTimeCode, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        OemCodeHi (Manufacturer Code of nodes that should accept this trigger)
    # 8:        OemCodeLo
    # 9:        Key (Trigger Key. If the oem value is manufacturer specific, unless the OEM code is set to 0xFFFF
    #           0: KeyAscii (SubKey Field contains an ASCII character which the receiving device should process as if
    #              it were a keyboard press.)
    #           1: KeyMacro (The SubKey contains the number of a number which the receiving device should execute
    #           2: KeySoft (The SubKey contains a soft-key number which the receiving device should process as if
    #              it was a soft-key keyboard press.)
    #           3: KeyShow (The SubKey field contains the number of a Show which the receivind device should run.)
    #           4-255: Undefined
    # 10:       SubKey (Trigger Sub Key)
    # 11:       Data (Payload, field not used if Key is set to 0-3)

    oem_code = calculate_hibyte(oem_code)
    if len(data) > 512:
        data = data[0:512]

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_TIME_CODE[1])  # OPCode Lo
    artnet_packet.append(OP_TIME_CODE[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x00)  # Filler 1
    artnet_packet.append(0x00)  # Filler 2
    artnet_packet.append(oem_code[1])  # OEM Code Hi
    artnet_packet.append(oem_code[0])   # OEM Code Lo
    artnet_packet.append(key)
    artnet_packet.append(subkey)
    if oem_code != 0xFFFF or key > 3:
        artnet_packet.extend(data)  # Payload

    artnet_output(artnet_packet, target_ip)


def artsync_output(target_ip="255.255.255.255"):
    # BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpSync, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Aux 1 (Transmit as zero.)
    # 6:        Aux 2 (Transmit as zero.)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_SYNC[1])  # OPCode Lo
    artnet_packet.append(OP_SYNC[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x0)  # Aux 1
    artnet_packet.append(0x0)  # Aux 2

    artnet_output(artnet_packet, target_ip)


def artnzs_output(artnet_data, target_ip="255.255.255.255"):
    # 0-39 DEVICES: UNICAST, 40+ DEVICES: BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpNzs, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Sequence (increment in the range 0x01 to 0xff. Set to 0x00 to disable the feature)
    # 6:        StartCode (DMX512 start code of this packet. Must not be zero or RDM!)
    # 7:        SubUni (Low Byte of the 15 bit Port-Address to which this packet is destined)
    # 8:        Net (Top 7 bits of the 15 bit Port-Address to which this packet is destined)
    # 9:        LengthHi (Length of the DMX512 data array. Should be between 2 and 512)
    # 10:       Lenght (Low Byte of above)
    # 11:       DMX512 data array

    length = calculate_hibyte(len(artnet_data["dmx_data"]))

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_NZS[1])  # OPCode Lo
    artnet_packet.append(OP_NZS[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(artnet_data["sequence_number"])  # Sequence <- ToDo
    artnet_packet.append(artnet_data["start_code"])  # Start code
    artnet_packet.append(artnet_data["universe_lobyte"])  # SubUni
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(length[0])  # LengthHi
    artnet_packet.append(length[1])  # Length
    artnet_packet.extend(bytearray(artnet_data["dmx_data"]))

    artnet_output(artnet_packet, target_ip)


def artvlc_output(artnet_data, target_ip="255.255.255.255", ieee=0, reply=0, beacon=0, transaction_number=0x0000,
                  slot_address=0, pay_check=0, vlc_depth=0, vlc_frequency=0, vlc_modulation=0, payload_language=0x0000,
                  repeat_frequency=0, payload=""):
    # 0-39 DEVICES: UNICAST, 40+ DEVICES: BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpNzs, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Sequence (increment in the range 0x01 to 0xff. Set to 0x00 to disable the feature)
    # 6:        StartCode (0x91, no other values are allowed!)
    # 7:        SubUni (Low Byte of the 15 bit Port-Address to which this packet is destined)
    # 8:        Net (Top 7 bits of the 15 bit Port-Address to which this packet is destined)
    # 9:        LengthHi (Length of the DMX512 data array. Should be between 2 and 512)
    # 10:       Lenght (Low Byte of above)
    # 11:       Vlc (Vlc Data packet)
    #           0: ManIdHi (0x41, magic number to identify the packet)
    #           1: ManIdLo (0x4C, magic number to identify the packet)
    #           2: SubCode (0x45, magic number to identify the packet)
    #           3: Flags
    #               5: Flags.Beacon (1=Repeat transmission until another packet is recived, 0=Transmit packt once)
    #               6: Flags.Reply (1=ReplyPacket in response to a request with matching transaction number,0= No Reply)
    #               7: Flags.Ieee (1=Shall be interpreted as IEEE VLC data. 0=PayLanguage defindes the payloads content)
    #           4: TransHi (16 bit transaction number to synchronize VLC transactions. 0x0000 = First packet of a
    #              transaction, 0xFFFF = Last packet of a transaction. Roll over to 0x0001 at 0xFFFE if it is not the
    #              last transaction
    #           5: TransLo (Lo Byte of above)
    #           6: SlotAddrHi (1-512 = the device to which this packet is directed. 0 = Add devices
    #           7: SlotAddrLo (Lo byte of above)
    #           8: PayCountHi (Payload Size in range 0 to 480
    #           9: PayCountLo (Lo byte of above)
    #           10: PayCheckHi (Unsigned additive checksum of the data in the payload)
    #           11: PayCheckLo (Lo Byte of above)
    #           12: Spare 1 (Transmit as zero, receivers don't test)
    #           13: VlcDepth (VLC modulation depth expressed as a percentage between 1 and 100. 0 = use default value)
    #           14: VlcFreqHi (Modulation Frequency expressed as Hz. A value of 0 inicates the default value)
    #           15: VlcFreqLo (Lo Byte of above)
    #           16: VlcModHi (Modulation type number the transmitter should use, 0x0000 = use default value)
    #           17: VlcModLo (Lo Byte of above)
    #           18: PayLangHi (16 bit language code)
    #               0x0000: Beacon URL (Payload contains a simple text string representing a URL)
    #               0x0001: Beacon Text (Payload contains a simple ASCII text message)
    #           19: PayLangLo (Lo Byte of above)
    #           20: BeacRepHi (If Flags.Beacon is set, this value indicated the frequency in Hz at which packets should
    #               be repeated. 0x0000 = Transmitter default
    #           21: BeacRepLo (Lo Byte of above)
    #           22: Payload (Actual Data)

    length = calculate_hibyte(len(artnet_data["dmx_data"]))
    flags = int(f"{ieee}{reply}{beacon}00000",2)
    transaction_number = calculate_hibyte(transaction_number)
    slot_address = calculate_hibyte(slot_address)
    pay_count = calculate_hibyte(len(payload))
    pay_check = calculate_hibyte(pay_check)
    vlc_frequency = calculate_hibyte(vlc_frequency)
    vlc_modulation = calculate_hibyte(vlc_modulation)
    payload_language = calculate_hibyte(payload_language)
    repeat_frequency = calculate_hibyte(repeat_frequency)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_NZS[1])  # OPCode Lo
    artnet_packet.append(OP_NZS[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(artnet_data["sequence_number"])  # Sequence <- ToDo
    artnet_packet.append(0x91)  # Start code
    artnet_packet.append(artnet_data["universe_lobyte"])  # SubUni
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(length[0])  # LengthHi
    artnet_packet.append(length[1])  # Length
    artnet_packet.append(0x41)  # Magic Number 1
    artnet_packet.append(0x4C)  # Magic Number 2
    artnet_packet.append(0x45)  # Magic Number 3
    artnet_packet.append(flags)  # Flags
    artnet_packet.append(transaction_number[1])  # TransHi
    artnet_packet.append(transaction_number[0])  # TransLo
    artnet_packet.append(slot_address[1])  # SlotAddrHi
    artnet_packet.append(slot_address[0])  # SlotAddrLo
    artnet_packet.append(pay_count[1])  # PayCountHi
    artnet_packet.append(pay_count[0])  # PayCountLo
    artnet_packet.append(pay_check[1])  # PayCheckHi <- ToDo
    artnet_packet.append(pay_check[0])  # PayCheckLo
    artnet_packet.append(0x0)  # Spare 1
    artnet_packet.append(vlc_depth)
    artnet_packet.append(vlc_frequency[1])
    artnet_packet.append(vlc_frequency[0])
    artnet_packet.append(vlc_modulation[1])
    artnet_packet.append(vlc_modulation[0])
    artnet_packet.append(payload_language[1])
    artnet_packet.append(payload_language[0])
    artnet_packet.append(repeat_frequency[1])
    artnet_packet.append(repeat_frequency[0])
    artnet_packet.extend(payload)

    artnet_output(artnet_packet, target_ip)


def artinput_output(target_ip="255.255.255.255", bind_index=1,
                    input_ports=0, input1=1, input2=1, input3=1, input4=1):
    # UNICAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpInput, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Bind Index (Defines the bound node which originated this packet and is used to uniquely identify the
    #           bound node when Identical IP addresses are in use. Represents the order of bound devices
    #           A lower number means closer to the root device. 1 = Root Device)
    # 7:        NumPortsHi (For future expansion and is currently zero)
    # 8:        NumPortsLo (Number of input and output ports. If number of output and inputs is not equal, the largest
    #           Number is taken. Maximum value is 4.
    # 9:        Input[4]
    #               0: 0 = Enabled, 1 = Disabled
    #               1-7: Not currently used

    input_ports = calculate_hibyte(input_ports)

    input1 = int(f"0000000{input1}", 2)
    input2 = int(f"0000000{input2}", 2)
    input3 = int(f"0000000{input3}", 2)
    input4 = int(f"0000000{input4}", 2)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_INPUT[1])  # OPCode Lo
    artnet_packet.append(OP_INPUT[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x0)          # Filler1
    artnet_packet.append(bind_index)   # Bind Index
    artnet_packet.append(input_ports[0])  # NumPortsHi
    artnet_packet.append(input_ports[1])  # NumPortsLo
    artnet_packet.append(input1)
    artnet_packet.append(input2)
    artnet_packet.append(input3)
    artnet_packet.append(input4)

    artnet_output(artnet_packet, target_ip)


def artfirmwaremaster_output(target_ip="255.255.255.255", firmware_type="FirmCont", block_id=0x00,
                             firmware_length=0x00000000, data=""):
    # UNICAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpFirmwareMaster, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        Type (Defines the packet content)
    #           0x00: FirmFirst (The First Packet of a firmware upload)
    #           0x01: FirmCont (A consecutive continuation packet of a firmware upload)
    #           0x02: FirmLast (The last packet of a firmware upload)
    #           0x03: UbeaFirst (The First Packet of a UBEA upload)
    #           0x04: UbeaCont (A consecutive continuation packet of a UBEA upload)
    #           0x05: UbeaLast (The last packet of a UBEA upload)
    # 8:        BlockId (Counts the consecutive blocks of firmware starting at 0x00 for the FirmFirst or UbeaFirst.)
    # 9:        FirmwareLength3 (Describes the total number of words in the firmware upload plus the firmware header
    #           size. Eg a 32K word upload plus 530 words of header information == 0x00008212. This value is also the
    #           file size (in words) of the file to be uploaded)
    # 10:       FirmwareLength2
    # 11:       FirmwareLength1
    # 12:       FirmwareLength0 (LSB of above)
    # 13:       Spare[20] (Ignore by receivers, set to zero by sender.)
    # 14:       Data (Hi Byte first interpretation is manufacturer specific. Final packet should be null terminated if
    #           less than 512 bytes are needed)

    if firmware_type == "FirmFirst":
        firmware_type = 0x00
    elif firmware_type == "FirmCont":
        firmware_type = 0x01
    elif firmware_type == "FirmLast":
        firmware_type = 0x02
    elif firmware_type == "UbeaFirst":
        firmware_type = 0x03
    elif firmware_type == "UbeaCont":
        firmware_type = 0x04
    elif firmware_type == "UbeaLast":
        firmware_type = 0x05

    firmware_length3 = (firmware_length >> 24 & 0xFF)
    firmware_length2 = (firmware_length >> 16 & 0xFF)
    firmware_length1 = (firmware_length >> 8 & 0xFF)
    firmware_length0 = (firmware_length & 0xFF)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_FIRMWARE_MASTER[1])  # OPCode Lo
    artnet_packet.append(OP_FIRMWARE_MASTER[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x0)          # Filler1
    artnet_packet.append(0x0)          # Filler2
    artnet_packet.append(firmware_type)  # Type
    artnet_packet.append(block_id)     # BlockId
    artnet_packet.append(firmware_length3)
    artnet_packet.append(firmware_length2)
    artnet_packet.append(firmware_length1)
    artnet_packet.append(firmware_length0)
    for i in range(20):
        artnet_packet.append(0x0)  # Spare
    artnet_packet.extend(data)     # Data

    artnet_output(artnet_packet, target_ip)


def artfirmwarereply_output(target_ip="255.255.255.255", firmware_type="FirmBlockGood"):
    # UNICAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpFirmwareReply, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        Type (Defines the packet content)
    #           0x00: FirmBlockGood (Last packet received successfully)
    #           0x01: FirmAllGood (All firmware received successfully)
    #           0xff: FirmFail (Firmware upload failed)
    # 8:        Spare (Ignore by receivers, set to zero by sender.)

    if firmware_type == "FirmBlockGood":
        firmware_type = 0x00
    elif firmware_type == "FirmAllGood":
        firmware_type = 0x01
    elif firmware_type == "FirmFail":
        firmware_type = 0xff

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_FIRMWARE_REPLY[1])  # OPCode Lo
    artnet_packet.append(OP_FIRMWARE_REPLY[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x0)  # Filler1
    artnet_packet.append(0x0)  # Filler2
    artnet_packet.append(firmware_type)  # Type
    for i in range(21):
        artnet_packet.append(0x0)  # Spare

    artnet_output(artnet_packet, target_ip)


def arttodrequest_output(artnet_data, target_ip="255.255.255.255", firmware_type="FirmBlockGood", command=0x00,
                         add_count=32):
    # BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpTodRequest, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        Spare 1 (Ignore by receivers, set to zero by sender.)
    # 8:        Spare 2 (Ignore by receivers, set to zero by sender.)
    # 9:        Spare 3 (Ignore by receivers, set to zero by sender.)
    # 10:       Spare 4 (Ignore by receivers, set to zero by sender.)
    # 11:       Spare 5 (Ignore by receivers, set to zero by sender.)
    # 12:       Spare 6 (Ignore by receivers, set to zero by sender.)
    # 13:       Spare 7 (Ignore by receivers, set to zero by sender.)
    # 14:       Net (Top 7 bits of the 15 bit Port-Address of nodes that must respond to this packet)
    # 15:       Command (0x00 = Tod Full - Send the entire TOD)
    # 16:       AddCount (The number of entries in Address that are used. Max value is 32.
    # 17:       Address[32] (Defines the low byte of the Port-Address of the Output Gateway nodes that must respond to
    #           this packet. The high nibble is the Sub-Net-Switch. The low nibble is the universe. Combined with the
    #           Net field, this is the 15 bit address.

    if firmware_type == "FirmBlockGood":
        firmware_type = 0x00
    elif firmware_type == "FirmAllGood":
        firmware_type = 0x01
    elif firmware_type == "FirmFail":
        firmware_type = 0xff

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_TOD_REQUEST[1])  # OPCode Lo
    artnet_packet.append(OP_TOD_REQUEST[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x0)  # Filler1
    artnet_packet.append(0x0)  # Filler2
    artnet_packet.append(0x0)  # Spare 1
    artnet_packet.append(0x0)  # Spare 2
    artnet_packet.append(0x0)  # Spare 3
    artnet_packet.append(0x0)  # Spare 4
    artnet_packet.append(0x0)  # Spare 5
    artnet_packet.append(0x0)  # Spare 6
    artnet_packet.append(0x0)  # Spare 7
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(command)  # Command
    artnet_packet.append(add_count)  # AddCount
    artnet_packet.append(artnet_data["universe_lobyte"])  # Address <- ToDo

    artnet_output(artnet_packet, target_ip)


def arttoddata_output(artnet_data, target_ip="255.255.255.255", rdm_version="standard", port=1, bind_index=1,
                      command_response=0x00, uid_total=0, block_count=0, tod=[]):
    # BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpTodData, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        RdmVer (RDM Draft V1.0 = 0x00, RDM Standard V1.0 = 0x01)
    # 6:        Port (Physical Port Range 1-4)
    # 7:        Spare 1 (Ignore by receivers, set to zero by sender.)
    # 8:        Spare 2 (Ignore by receivers, set to zero by sender.)
    # 9:        Spare 3 (Ignore by receivers, set to zero by sender.)
    # 10:       Spare 4 (Ignore by receivers, set to zero by sender.)
    # 11:       Spare 5 (Ignore by receivers, set to zero by sender.)
    # 12:       Spare 6 (Ignore by receivers, set to zero by sender.)
    # 13:       BindIndex (Defines the bound node which originated the packet. In combination with Port and Source IP
    #           address, it uniquely identifies the sender. This must match the BindIndex field in ArtPollReply. This
    #           number represents the order of bound devices. 1 = Root device
    # 14:       Net (Top 7 bits of the 15 bit Port-Address of nodes that must respond to this packet)
    # 15:       Command Response
    #           0x00: TodFull (Counts the entire TOD or is the first packet in a sequence of packets w. the entire TOD)
    #           0xff: TodNak (TOD is not available or discovery is incomplete)
    # 16:       Address[32] (Defines the low byte of the Port-Address of the Output Gateway nodes that must respond to
    #           this packet. The high nibble is the Sub-Net-Switch. The low nibble is the universe. Combined with the
    #           Net field, this is the 15 bit address.
    # 17:       UidTotalHi (The total number of devices discovered by this universe)
    # 18:       UidTotalLo (Lo Byte of above)
    # 19:       BlockCount (The index number of this packet. When UID exceeds 200, multiple ArtTodData packets are used.
    #           BlockCount is set to zero for the first packet and incremented for each subsequent packet containing
    #           blocks of TOD information
    # 20:       UidCount (The number of UIDs encoded in this packet. This is the index of the following array.
    # 21:       ToD[UidCount] (48 bit array of RDM UIDs)

    if rdm_version == "draft":
        rdm_version = 0x00
    elif rdm_version == "standard":
        rdm_version = 0x01
    uid_total = calculate_hibyte(uid_total)

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_TOD_DATA[1])  # OPCode Lo
    artnet_packet.append(OP_TOD_DATA[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(rdm_version)  # RdmVer
    artnet_packet.append(port)  # Port
    artnet_packet.append(0x0)  # Spare 1
    artnet_packet.append(0x0)  # Spare 2
    artnet_packet.append(0x0)  # Spare 3
    artnet_packet.append(0x0)  # Spare 4
    artnet_packet.append(0x0)  # Spare 5
    artnet_packet.append(0x0)  # Spare 6
    artnet_packet.append(bind_index)  # Bind Index <- ToDo
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(command_response)  # Comamnd Response
    artnet_packet.append(artnet_data["universe_lobyte"])  # Address <- ToDo
    artnet_packet.append(uid_total[0])  # UidTotalHi
    artnet_packet.append(uid_total[1])  # uidTotalLo
    artnet_packet.append(block_count)  # BlockCount
    artnet_packet.append(len(tod))  # UidCount
    for i in range(len(tod)):
        artnet_packet.append(tod[i])  # ToD

    artnet_output(artnet_packet, target_ip)


def arttodcontrol_output(artnet_data, target_ip="255.255.255.255", command_response=0x00):
    # BROADCAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpTodControl, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        Filler 1 (Ignore by receivers, set to zero by sender.)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        Spare 1 (Ignore by receivers, set to zero by sender.)
    # 8:        Spare 2 (Ignore by receivers, set to zero by sender.)
    # 9:        Spare 3 (Ignore by receivers, set to zero by sender.)
    # 10:       Spare 4 (Ignore by receivers, set to zero by sender.)
    # 11:       Spare 5 (Ignore by receivers, set to zero by sender.)
    # 12:       Spare 6 (Ignore by receivers, set to zero by sender.)
    # 13:       Spare 7 (Ignore by receivers, set to zero by sender.)
    # 14:       Net (Top 7 bits of the 15 bit Port-Address of nodes that must respond to this packet)
    # 15:       Command
    #           0x00: AtcNone (No action)
    #           0x01: AtcFlush (Node flushes its TOD and instigates full discovery)
    # 16:       Address (Defines the low byte of the Port-Address of the Output Gateway nodes that should action this
    #           command. The high nibble is the Sub-Net-Switch. The low nibble is the universe. Combined with the
    #           Net field, this is the 15 bit address.

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_TOD_CONTROL[1])  # OPCode Lo
    artnet_packet.append(OP_TOD_CONTROL[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(0x0)  # Filler 1
    artnet_packet.append(0x0)  # Filler 2
    artnet_packet.append(0x0)  # Spare 1
    artnet_packet.append(0x0)  # Spare 2
    artnet_packet.append(0x0)  # Spare 3
    artnet_packet.append(0x0)  # Spare 4
    artnet_packet.append(0x0)  # Spare 5
    artnet_packet.append(0x0)  # Spare 6
    artnet_packet.append(0x0)  # Spare 7
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(command_response)  # Comamnd Response
    artnet_packet.append(artnet_data["universe_lobyte"])  # Address <- ToDo

    artnet_output(artnet_packet, target_ip)


def artrdm_output(artnet_data, target_ip="255.255.255.255", rdm_version="standard", command_response=0x00):
    # BROADCAST or UNICAST (UNICAST is preferred)
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpRdm, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        RdmVer (RDM Draft V1.0 = 0x00, RDM Standard V1.0 = 0x01)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        Spare 1 (Ignore by receivers, set to zero by sender.)
    # 8:        Spare 2 (Ignore by receivers, set to zero by sender.)
    # 9:        Spare 3 (Ignore by receivers, set to zero by sender.)
    # 10:       Spare 4 (Ignore by receivers, set to zero by sender.)
    # 11:       Spare 5 (Ignore by receivers, set to zero by sender.)
    # 12:       Spare 6 (Ignore by receivers, set to zero by sender.)
    # 13:       Spare 7 (Ignore by receivers, set to zero by sender.)
    # 14:       Net (Top 7 bits of the 15 bit Port-Address of nodes that must respond to this packet)
    # 15:       Command
    #           0x00: ArProcess (Process RDM Packet)
    # 16:       Address[32] (Defines the low byte of the Port-Address that should action this command.
    #           The high nibble is the Sub-Net-Switch. The low nibble is the universe. Combined with the
    #           Net field, this is the 15 bit address.
    # 17:       RdmPacket (The RDM data packet excluding the DMX StartCode.

    if rdm_version == "draft":
        rdm_version = 0x00
    elif rdm_version == "standard":
        rdm_version = 0x01

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_RDM[1])  # OPCode Lo
    artnet_packet.append(OP_RDM[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(rdm_version)  # RdmVer
    artnet_packet.append(0x0)  # Filler 2
    artnet_packet.append(0x0)  # Spare 1
    artnet_packet.append(0x0)  # Spare 2
    artnet_packet.append(0x0)  # Spare 3
    artnet_packet.append(0x0)  # Spare 4
    artnet_packet.append(0x0)  # Spare 5
    artnet_packet.append(0x0)  # Spare 6
    artnet_packet.append(0x0)  # Spare 7
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(command_response)  # Command Response
    artnet_packet.append(artnet_data["universe_lobyte"])  # Address <- ToDo
    artnet_packet.append(artnet_packet["rdm_data"])  # RDM Packet

    artnet_output(artnet_packet, target_ip)


def artrdmsub_output(artnet_data, target_ip="255.255.255.255", rdm_version="standard", uid=0x000000000000, command_response=0x00, ):
    # UNICAST
    # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
    # 2:        OPCode (OpRdmSub, see OPCode list) -> Int16!
    # 3:        ProtVerHi (0x0)
    # 4:        ProtVerLo (14)
    # 5:        RdmVer (RDM Draft V1.0 = 0x00, RDM Standard V1.0 = 0x01)
    # 6:        Filler 2 (Ignore by receivers, set to zero by sender.)
    # 7:        UID (UID of target RDM device. The UID is a 48-bit ID containing a 16-bit manufacturer ID and a 32-bit
    #           device ID.)
    # 8:        Spare 1 (Ignore by receivers, set to zero by sender.)
    # 9:        CommandClass (Defines whether this is a "Get", "Set", "GetResponse" or "SetResponse")
    # 10:       ParameterIp (As per RDM specification. Defines the type of parameter contained by this packet.)
    # 10:       Lo Byte of above
    # 11:       SubDevice (Defines the first device information contained in packet. 0 = Root device,
    #           1 = First subdevice)
    # 11:       Lo Byte of above
    # 12:       SubCount (Number of sub devices packed into this packet. Zero is illegal!
    # 12:       Lo Byte of above
    # 13:       Spare 2 (Ignore by receivers, set to zero by sender.)
    # 14:       Spare 3(Ignore by receivers, set to zero by sender.)
    # 15:       Spare 4 (Ignore by receivers, set to zero by sender.)
    # 16:       Spare 5 (Ignore by receivers, set to zero by sender.)
    # 17:       Data (Packed 16 bit big-endian data. The size of the data array is defined by the contents of
    #           CommandClass and SubCount
    #           Get: Size = 0
    #           Set: Size = SubCount
    #           GetResponse: Size = SubCount
    #           SetResponse: Size = 0

    if rdm_version == "draft":
        rdm_version = 0x00
    elif rdm_version == "standard":
        rdm_version = 0x01

    artnet_packet = bytearray()
    artnet_packet.extend(ID)
    artnet_packet.append(OP_RDM_SUB[1])  # OPCode Lo
    artnet_packet.append(OP_RDM_SUB[0])  # OPCode Hi
    artnet_packet.append(PROT_VER_HI)  # ProtVerHi
    artnet_packet.append(PROT_VER_LO)  # ProtVerLo
    artnet_packet.append(rdm_version)  # RdmVer
    artnet_packet.append(0x0)  # Filler 2
    artnet_packet.append(uid)  # UID
    artnet_packet.append(0x0)  # Spare 1
    artnet_packet.append(0x0)  # Spare 3
    artnet_packet.append(0x0)  # Spare 4
    artnet_packet.append(0x0)  # Spare 5
    artnet_packet.append(0x0)  # Spare 6
    artnet_packet.append(0x0)  # Spare 7
    artnet_packet.append(artnet_data["universe_hibyte"])  # Net
    artnet_packet.append(command_response)  # Command Response
    artnet_packet.append(artnet_data["universe_lobyte"])  # Address <- ToDo
    artnet_packet.append(artnet_packet["rdm_data"])  # RDM Packet

    artnet_output(artnet_packet, target_ip)


def identify_artnet_packet(input):
    # Extracts the type of ArtNet packet and will return the type of packet and the packet itself.
    if len(input) < 1:
        raise TypeError("Unknown Package. The minimum length for a sACN package is ...")  # <- ToDo
    if input[8] == OP_DMX[1] and input[9] == OP_DMX[0]:
        print("DMX PACKET")
    elif input[8] == OP_POLL[1] and input[9] == OP_POLL[0]:
        print("ART POLL")
        #artpollreply_output(PRIMARY_ARTNET_ADDRESS,)
    elif input[8] == OP_POLL_REPLY[1]and input[9] == OP_POLL_REPLY[0]:
        print("ART POLL REPLY")


def artnet_output(artnet_packet, target_ip):
    try:
        set_artnet_sock.sendto(artnet_packet, (target_ip, UDP_PORT))
        # print(f"Sending {artnet_packet} to {target_ip}")
    except Exception as exception:
        print(f"Socket error: {exception}")
