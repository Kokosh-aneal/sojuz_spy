#! /usr/bin/python3

#If u want to have logs in diffrent directory u can change it here
#Default it is storaged in directory where this program is
path_to_log_file = ""

#Path to directory where you install this tool
#It's important for Report class, to change directory to tmp
reporter_dir = ''

#URL to API of your Zabbix server
#Default url (from Zabbix documentation) is: http://company.com/zabbix/api_jsonrpc.php
api_url = ''

#Login and password to api - you have to create API user in order to use this tool
#You can use another one of course which you have created before
api_login = ''
api_pass = ''

#Configuration of your mail server
smtp_server = ''
smtp_port = 

#Login and password to mail account, from which reports will be sent
email_login = ''
email_pass = ''

#Here u can specify recipients
#recipients = 'user1@mail.server.com,user2@mail.server.com,user3@mail.server.com'
recipients = ''

#If you want, you can add your company logo at the bottom of every page, just add path to image
#in .jpeg format
company_logo_path = 
