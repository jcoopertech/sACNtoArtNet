import threading
from load_settings import load_settings
from server.main import main as run
from artnet import main as artnet
from sacn import main as sacn
import webbrowser


class Thread(threading.Thread):
    def __init__(self, thread_id, name):
        Thread.__init__(self)
        self.thread_id = id
        self.name = name

    def stop(self):
        self._stop.set()


def main():
    """Start Server and converters"""

    '''Server'''
    server = threading.Thread(target=run)
    server.start()
    # webbrowser.open(f"http://{load_settings('ip', 'Server')}:{load_settings('server_port', 'Server')}", 0)

    '''Converters'''
    sacn_artnet = threading.Thread(target=sacn.sacn_to_artnet)
    sacn_artnet.start()
    print("sACN -> Art-Net converter started!")

    artnet_sacn = threading.Thread(target=artnet.artnet_to_sacn)
    artnet_sacn.start()
    print("Art-Net -> sACN converter started!")


if __name__ == "__main__":
    main()
