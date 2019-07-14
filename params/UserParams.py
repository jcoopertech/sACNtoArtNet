"""USER Defined Parameters"""
universe_min = 1
universe_max = 20
use_per_channel_priority = False  # Activate to use per channel priority packets (0xDD start code packets)
merge = False  # Activate if using more than one source in the network
artnet_to_sacn = True
sacn_to_artnet = False
broadcast = True  # Normally, unicast should be used to talk to ArtNet devices. Some old devices don't send ArtPolls,
#                   # so you have to disable unicast and send broadcast.
ip = "0.0.0.0"  # Your IP. Set to "0.0.0.0" to use your device IP
debug_level = 3  # 1 = Print critical errors, 2 = Print all errors, 3 = Print errors and info messages,
#                # 4 = Print errors, info messages and debug information, 0 = disabled
