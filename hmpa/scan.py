import sys
import os
import platform
import subprocess


def which(program):
    """Determines whether program exists
    """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file


def parse_mac_rssi(raw_output):
    found_macs = {}
    for line in raw_output.decode('utf-8').split('\n'):
        if line.strip() == '':
            continue

        dats = line.split()

        if len(dats) == 3:
            if ':' not in dats[0]:
                continue
            mac = dats[0]
            if mac not in found_macs:
                found_macs[mac] = []
            rssi = float(dats[2])
            found_macs[mac].append(rssi)

    for key, value in found_macs.items():
        found_macs[key] = float(sum(value)) / float(len(value))

    return found_macs


def scan(adapter, scantime, sort=False):
    try:
        tshark = which("tshark")
    except:
        if platform.system() != 'Darwin':
            print('tshark not found, install using\n\napt-get install tshark\n')
        else:
            print('wireshark not found, install using: \n\tbrew install wireshark')
            print('you may also need to execute: \n\tbrew cask install wireshark-chmodbpf')
        return

    # Scan with tshark
    command = [tshark, '-I', '-i', adapter, '-a',
               'duration:' + scantime, '-w', '/tmp/tshark-temp']
    run_tshark = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = run_tshark.communicate()
    print(command)

    command = [
        tshark, '-r',
        '/tmp/tshark-temp', '-T',
        'fields', '-e',
        'wlan.sa', '-e',
        'wlan.bssid', '-e',
        'radiotap.dbm_antsignal'
    ]
    run_tshark = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = run_tshark.communicate()
    found_macs = parse_mac_rssi(output)
    print(found_macs)



if __name__ == '__main__':
    adapter = 'wlan1'
    scan(adapter, '10')