#! /usr/bin/python3

import json

# Requests used by Session

#Authentification request
def auth_req(login,password):
    auth = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": login,
            "password": password 
        },
        "id": 1,
        "auth": None
    }
    return json.dumps(auth)

#Request to get list of hosts
def host_list_req(auth):
    req = {
        "jsonrpc":"2.0",
        "method":"host.get",
        "params":{
            "output": [
                "hostid","name"
            ],
            "tags":[
                {
                "tag":"report",
                "value":"1",
                "operator":"0"
                }
            ]
        },
        "auth": auth,
        "id": 2
    }
    return json.dumps(req)

#Request to get items of chosen host
def host_item_req(auth,host_id):
    req = {
        "jsonrpc": "2.0",
        "method":"item.get",
        "params": {
            "output": ["itemid","name","key_","units"],
            "hostids": host_id,
            "application":"report"
        },
        "id":3,
        "auth":auth
    }
    return json.dumps(req)

#Request to get history of chosen item in chosen time
def item_history_req(auth,item_id,time_from,time_till,history):
    req = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "history": history,
            "itemids": item_id,
            "time_from": time_from,
            "time_till": time_till,
            },
        "auth": auth,
        "id": 2
    }
    return json.dumps(req)
