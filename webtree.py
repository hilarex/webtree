# coding: utf-8

import sys
import requests
import re
from termcolor import colored
import argparse
from base64 import b64encode

# ---- Disabling SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# ----

def parse(url, extensions, level, auth=""):
    
    if auth is not None:
        headers = {'Authorization':'Basic {}'.format(auth)}
        response = requests.get(url,headers=headers,verify=False)
    else:
        response = requests.get(url,verify=False)

    if "<title>index of" in response.text.lower():
        links = re.findall('href=\"(?!\?)([^>]*)\"(?!>parent directory)', response.text.lower())
        for i in range(len(links)):
            if links[i][-1] == "/":
                is_directory = 1
                name = colored(links[i],'blue')
            else:
                is_directory = 0
                name = links[i]
            if i == len(links)-1:
                delimiter = "└──"
            else:
                delimiter = "├──"
            if name.split('.')[-1].lower() not in extensions:
                print("│   " + "│   "*level + delimiter + name)
    
            if is_directory:
                parse(url.strip("/")+"/"+links[i], extensions, level+1)
    else:
        print("│   " + "│   "*level +"listing not enable")
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url with directory listing")
    parser.add_argument("-e",'--extension', default='', help="exclude these extensions on print") 
    parser.add_argument("-u",'--user', default='', help="Basic Authentication username") 
    parser.add_argument("-p",'--password', default='', help="Basic Authentication password") 
    args = parser.parse_args()

    print(colored(args.url, 'green'))
    if args.user and args.password:
        auth_header = b64encode('{}:{}'.format(args.user,args.password).encode('utf-8'))
        parse(args.url, args.extension.split(','), 0, auth_header.decode('utf-8'))
    else:
        parse(args.url, args.extension.split(','), 0)
