#! /usr/bin/python3

import smtplib
from setup.config import *
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import sys

class Mail:
#Mail class constructor
    def __init__(self,log,today,file_data,file_type,file_name):
        self.log = log
        self.log.append(2,'Creating email message')
        self.msg = MIMEMultipart()
        opt = sys.argv[1:][0]
        print(opt)
        if opt == '-d':
            self.msg['Subject'] = '[ZABBIX][{}] Daily report'.format(today)
        elif opt == '-m':
            self.msg['Subject'] = '[ZABBIX][{}] Monthly report'.format(today)
        elif opt == '-w':
            self.msg['Subject'] = '[ZABBIX][{}] Weekly report'.format(today)
        else:
            self.msg['Subject'] = '[ZABBIX][{}] Report'.format(today)
        self.msg['From'] = email_login
        self.msg['To'] = recipients
        attach = MIMEApplication(file_data,subtype=file_type)
        attach.add_header('Content-Disposition','attachment',filename=str(file_name))
        self.msg.attach(attach)
        self.log.append(2,'Created email message')

#SEND
#Function which sends mail to recipients defined in config.py
    def send(self):
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            self.log.append(2,'Sending report to ' + str(recipients))
            server.starttls()
            server.login(email_login,email_pass)
            server.send_message(self.msg)
