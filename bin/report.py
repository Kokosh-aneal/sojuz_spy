#! /usr/bin/python3

from bin.session import Session
from bin.mail import Mail
from datetime import datetime 
import imghdr
from setup.config import *
import os

#Reportlab modules
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class Report:
#Report class constructor
    def __init__(self,log, t_from, t_to):
        self.log = log
        self.log.append(2,'Starting new ZABBIX API session')
        self.session = Session(log)
        self.now = datetime.now()
        self.today_string = self.now.strftime('%d.%m.%Y')
        self.t_from = int(t_from)
        self.t_to = int(t_to)
        self.report_title = 'zabbix_report_' + self.today_string
        self.report_name = self.report_title + ".pdf"

#GET_DATA
#Getting data from zabbix via session class
    def get_data(self):
        self.log.append(2,'Starting to gather data from API')
        self.host_list = self.session.gen_host_list()
        self.session.gen_host_items(self.host_list)
        self.log.append(2,'Data gathered successfully')

#GEN_REPORT
#Creating report and saving it in /tmp/ dir
    def gen_report(self):
        #First page
        self.log.append(2,'Generating report')
        c = canvas.Canvas(self.report_name, pagesize=letter)
        w, h = letter
        c.setTitle(self.report_title)
        c.setFont('Times-Roman',140)
        c.drawString(50,575,'ZABBIX')
        c.setFont('Times-Roman',18)
        delta = (self.t_to-self.t_from)/(60*60)
        unit = 'h'
        if delta > 24:
            delta=delta/24
            unit = 'days'
        aands = 'analysis and statystics from last: ' + str(delta) + ' ' + unit
        c.drawString(50,550,aands)
        c.drawString(480,550,self.today_string)
        c.setFont('Times-Roman',10)
        if 'company_logo_path' in globals():
            if os.path.isfile(company_logo_path):
                c.drawImage(company_logo_path,w-(4*40),10,width=3.5*40,height=40)
        c.showPage()
        #Creating graphs, inserting them into the report
        os.chdir(reporter_dir+'tmp')
        for host in self.host_list:
            c.drawString(50,742,host.name)
            c.line(50,740,550,740)
            y =590 
            for item in host.item_list:
                if y < 100:
                    c.drawImage(company_logo_path,w-(4*40),10,width=3.5*40,height=40)
                    c.showPage()
                    y = 590
                self.session.gen_item_history(item,str(self.t_from),str(self.t_to))
                item.gen_graph()
                c.drawImage(item.ID+'.jpg',0,y,width=600,height=150)
                y = y - 160
                os.remove(item.ID + '.jpg')
            if 'company_logo_path' in globals():
                if os.path.isfile(company_logo_path):
                    c.drawImage(company_logo_path,w-(4*40),10,width=3.5*40,height=40)
            c.showPage()
        c.save()
        self.log.append(2,'Report generated successfully')

#SEND_REPORT
#Sending report to recipients given in config
    def send_report(self):
        with open(self.report_name,'rb') as f:
            self.file_data = f.read()
            self.file_type = imghdr.what(f.name)
            self.file_name = f.name
        mail = Mail(self.log,self.today_string,self.file_data,self.file_type,self.file_name)
        mail.send()

#Report class destructor
    def __del__(self):
        if os.path.isfile(self.report_name):
            self.log.append(2,'Report created and sent to recipients successfully')
            os.remove(self.report_name)
        else:
            self.log.append(2,'Something went wrong. Report has not been generated.')
