#! /usr/bin/python3

from setup.config import *
from bin.zabbix_requests import *
from bin.logger import *
from bin.host import Host
from bin.item import Item
from datetime import datetime, date, timedelta
import requests
import json

#Variable used in all requests
ctype = {'Content-type':'application/json-rpc'}

class Session:
#Session class constructor, opens session with api and creates auth code which is used in further requests to Zabbix API
    def __init__(self,log):
        self.log = log
        self.Host_list = []
        log.append(2,'Sending auth request to zabbix')
        r = requests.post(api_url,auth_req(api_login,api_pass),headers=ctype) 
        if r.status_code == 200:
            content = json.loads(r.content)
            if 'result' in content:
                log.append(2,'Authentification ended with success')
                self.auth = content['result']
            else:    
                log.append(4,'Authentification failed. API:' + str(content['error']))
                exit(-1)
        else:
            log.append(4,'Connection failed. Code:' + str(r.status_code))
            exit(-1)

#GEN_HOST_LIST
#Creates list of hosts from Zabbix which are contained in report
    def gen_host_list(self):
        self.log.append(2,'Sending host list request to zabbix')
        r = requests.post(api_url,host_list_req(self.auth),headers=ctype)
        if r.status_code == 200:
            content = json.loads(r.content)
            if 'result' in content:
                self.log.append(2,'Host list request ended with success')
                host_list = content['result']
                tmp_host_list = []
                for idx, host in enumerate(host_list):
                    tmp_host_list.append(Host(host['hostid'],host['name'],self.log))
                self.log.append(2,'List of hosts created')
            else:    
                self.log.append(4,'Getting host list failed. API:' + str(content['error']))
                exit(-1)
        else:
            self.log.append(4,'Connection failed. Code:' + str(r.status_code))
            exit(-1)
        return tmp_host_list

#GEN_HOST_ITEMS
#Creates items of hosts which are contained in report
    def gen_host_items(self, host_list):
        self.log.append(2,'Sending host items request to zabbix')
        for idx, host in enumerate(host_list):
            r = requests.post(api_url,host_item_req(self.auth,host.ID),headers=ctype)
            if r.status_code == 200:
                content = json.loads(r.content)
                if 'result' in content:
                    for jdx, item in enumerate(content['result']):
                        host.item_list.append(Item(item['itemid'],item['name'],item['key_'],self.log,host.name,item['units']))
                    self.log.append(2,'Generated list of items for ' + host.name)
                else:
                    self.log.append(4,'Getting item failed. API: ' + str(content['error']))
                    exit(-1)
            else:
                self.log.append(4,'Connection failed. Code: ' + str(r.status_code))
                exit(-1)

#GEN_ITEM_HISTORY
#Downloads history of items from Zabbix API
    def gen_item_history(self, item, t_from, t_to):
        self.log.append(2,'Sending ' + item.name + ' history request to zabbix')
        history = 3
        r = requests.post(api_url,item_history_req(self.auth,item.ID,t_from,t_to,history),headers=ctype)
        if r.status_code == 200:
            content = json.loads(r.content)
            if 'result' in content:
                self.log.append(2,'Creating x and y for: ' + item.name)
                history = 0
                result = content['result']
                while len(result) == 0 and history<5:
                    self.log.append(2,'Entered while for ' + item.name+ 'current history:' + str(history) +  ' | current x:' + str(item.x))
                    r = requests.post(api_url,item_history_req(self.auth,item.ID,t_from,t_to,history),headers=ctype)
                    content = json.loads(r.content)
                    result = content['result']
                    history=history+1
                for idx, sample in enumerate(content['result']):
                    item.x.append(datetime.fromtimestamp(int(sample['clock'])))
                    item.y.append(float(sample['value']))
            else:
                tmp_log = 'Getting history of item ' + str(item.name) + ' failed. API: ' + str(content['error'])
                self.log.append(4,tmp_log)
                exit(-1)
        else:
            self.log.append(4,'Connection failed. Code: ' + str(r.status_code))
            exit(-1)
