import time
from datetime import datetime
import schedule

from hmpa import tshark
from config import config
from hmpa import serverchan
from hmpa import email


def brief_report(devices):
    all_devices = devices['found_devices']
    title = "{time} 一共扫描到 {sum} 台设备".format(time=devices['time'],
                                            sum=len(all_devices))
    content = ''
    for dev in all_devices:
        content += '- {mac} {rssi} {company} \n'.format(mac=dev['mac'],
                                                        rssi=int(dev['rssi']),
                                                        company=dev['company'])
    return title, content


def job():
    adapter = config.adapter
    devices = tshark.scan(adapter, 50)
    title, content = brief_report(devices)

    if config.use_email:
        print('send email notification')
        mail = email.Email(config.email['user'],
                           config.email['password'],
                           config.email['host'],
                           config.email['port'])
        mail.send(config.email['to_user'],
                  title,
                  content.split('\n'))

    if config.use_wechat:
        print('send wechat notification')
        serverchan.push(config.serverchan['sckey'], title, content=content)


if __name__ == '__main__':
    # while True:
    #     job()
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
