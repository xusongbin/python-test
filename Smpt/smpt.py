
import smtplib
from email.mime.text import MIMEText

import poplib

import re
import base64
from urllib import request

smtpserver = 'smtp.163.com'
poperver = 'pop.163.com'
username = 'ak3336105@163.com'
userpwd = '52023921033'

receiver = 'ak3336105@163.com'


def email_send(subject, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = receiver
    s = smtplib.SMTP(smtpserver, 25)
    try:
        # s.set_debuglevel(1)
        s.login(username, userpwd)
        s.sendmail(username, receiver, msg.as_string())
        return True
    except:
        s.quit()
    return False


def email_recv():
    s = poplib.POP3(poperver)
    try:
        s.user(username)
        s.pass_(userpwd)
    except:
        return ''
    resp, mails, octets = s.list()
    if len(mails) < 1:
        return ''
    _msg = ''
    for i in range(1, len(mails)+1):
        resp, lines, octets = s.retr(i)
        s.dele(i)
        if b'+OK' not in resp:
            continue
        msg_content = lines[len(lines)-1].decode('utf-8')
        print(msg_content)
        if re.match(r'^[A-Za-z0-9+/]*={0,2}$', msg_content):
            msg_content = base64.b64decode(msg_content).decode('utf-8')
        if '外网IP：' in msg_content:
            _msg = str(msg_content).split('：')[1]
    s.quit()
    return _msg


def get_public_ip():
    r = request.urlopen('http://ip.42.pl/raw')
    ip = r.read().decode('utf-8')
    if re.match(r'\d+\.\d+\.\d+\.\d+', ip):
        return ip
    return ''


if __name__ == '__main__':
    # ip = get_public_ip()
    # if ip != '':
    #     if email_send('获取外网IP地址', '外网IP：' + ip):
    #         print('发送成功')
    #     else:
    #         print('发送失败')
    print(email_recv())
