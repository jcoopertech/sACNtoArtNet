# sACNtoArtNet
This is the rewritten version of the decrecated sACNtoArtNet converter. 
It is a simple python script that is not using a single class. It converts sACN (aka. ANSI E1.31) to ArtNet (and vice versa in the future)
### Please Note:
It is necessary to run Python 3.6 or later for the script to run!


## Installation:
1. Download Python from https://www.python.org/downloads/
2. Download or clone the repository. 
3. From the terminal, run **main.py** Thats it.

The script will print out the type of received packet. Edit **socket_settings.py** to change the input universes (*universe_min* and *universe_max*), the merge mode (*merge* and *use_per_channel_priority* or the IP addresses to listen and send to. Please note: sACNtoArtNet will automatically bind to the needed multicast addresses for the universes between *universe_min* and *universe_max*.

### Tested platforms
- Windows 10
- Ubuntu Mate (Raspberry Pi)
- Raspbian (Note: Install Python 3.6 or later manually!)

## Currently working features:
- Convert sACN to ArtNet
- sACN priorities
- Answer to ArtPoll packets

## Known Problems:
- ArtNet will always send Broadcast

## Work in progress:
- Convert ArtNet to sACN
- Universe shifting
- GUI for the settings
- Unicast / Broadcast
- Make an Input-Patch for every single address

## Upcoming features:
- E1.33 packets, as soon it gets ratified by ESTA
- In the future, IPv6 shall be supported

### Please send me a message with feature requests and post some issues you have!
