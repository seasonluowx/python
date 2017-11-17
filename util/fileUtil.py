import sys

import os

crupath = sys.path[0]


def get_pid():
    print(os.path.join(crupath, 'logs/userId.txt'))
    with open(os.path.join(crupath, 'logs/userId.txt'), 'r',encoding='utf-8-sig') as fdm:
        line = fdm.readline().strip()
        if line == '':
            return 'userId login fail!'
        return line

def writeRecord(record):
    with open(os.path.join(crupath, 'logs/record.txt'), 'w', encoding='utf-8-sig') as recordf:
        recordf.write(record)

def writeEmailText(emailText):
    with open(os.path.join(crupath, 'logs/email.txt'), 'w', encoding='utf-8-sig') as emailf:
        emailf.write(emailText)

def writeAuth(authText):
    with open(os.path.join(crupath, 'logs/author.txt'), 'w', encoding='utf-8-sig') as authf:
        authf.write(authText)