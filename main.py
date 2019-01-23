from hmpa import tshark
from hmpa import oui

if __name__ == '__main__':
    adapter = 'wlan1'
    devices = tshark.scan(adapter, 10)
    print(devices)
