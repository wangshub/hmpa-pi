# -*- coding: utf-8 -*-
import time
from datetime import datetime
import schedule

from hmpa import tshark
from config import config
from hmpa import serverchan
from hmpa import email


def brief_report(devices):
    all_devices = devices['found_devices']
    title = "{time} 一共发现了 {sum} 台设备".format(time=devices['time'],
                                            sum=len(all_devices))
    content = 'Known Devices:    \n'

    for dev in all_devices:
        if dev['mac'] in list(config.known_devices.keys()):
            content += '{name}    \n'.format(name=config.known_devices[dev['mac']])

    content += 'All Devices:    \n'

    for dev in all_devices:
        content += '- {mac} {rssi} {company} \n'.format(mac=dev['mac'],
                                                        rssi=int(dev['rssi']),
                                                        company=dev['company'])
    return title, content


def job():
    adapter = config.adapter
    devices = tshark.scan(adapter, 60)
    title, content = brief_report(devices)

    if config.use_email:
        try:
            print('send email notification')
            mail = email.Email(config.email['user'], config.email['password'], config.email['host'], config.email['port'])
            mail.send(config.email['to_user'], title, content.split('\n'))
        except Exception as err:
            print(err)

    if config.use_wechat:
        try:
            print('send wechat notification')
            serverchan.push(config.serverchan['sckey'], title, content=content)
        except Exception as err:
            print(err)


if __name__ == '__main__':
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
