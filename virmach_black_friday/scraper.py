import time
import contextlib
from urllib.request import urlopen, Request, HTTPError
from bs4 import BeautifulSoup
import json

usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    }

def page_fetch(url):
    request = Request(url, headers=usr_agent)
    page = b''
    try:
        stream = urlopen(request)
        page = stream.read()
    except HTTPError as e:
        return b''
    
    return page

class VirmachConfig():
    def __init__(self):
        self.virt = '' # 'KVM'
        self.price = 0.0
        self.cpu = 0
        self.ram = 0
        self.hdd = 0
        self.bw = 0
        self.ips = 0
        self.pid = 0
        self.loc_state = ''
        self.loc_city = ''
        self.message = ""
        self.windows = False
        self.ended = False
    
        self.valid = False

def virmach_get_black_fridy_price():
    #
    # page_url = 'https://virmach.com/black-friday-cyber-monday/'
    #
    json_url = 'https://billing.virmach.com/modules/addons/blackfriday/new_plan.json'
    
    page = page_fetch(json_url)

    vm = VirmachConfig()

    if not page:
        return vm

    json_content = json.loads(page)

    # 1. ended?, if NOT ended, there's no ended field
    try:
        vm.ended = bool(json_content['ended'])
    except KeyError as e:
        vm.ended = False

    try:
        price = json_content['price']
        location = json_content['location']
        vm.virt = json_content['virt'] # "KVM"
        vm.cpu = json_content['cpu'] # int, number of cpu cores
        vm.ram = int(json_content['ram']) # ram is in string "1024"
        vm.hdd = json_content['hdd']
        vm.bw = json_content['bw'] # bandwidth
        vm.ips = json_content['ips'] # number of IP addresses
        vm.pid = json_content['pid'] # NO idea what this is
        vm.message = json_content['message']
    except KeyError as e:
        return vm

    # extract price    
    vm.price = float(price.split(' ')[0].split('$')[1])

    # extract city, state
    vm.city, vm.state = location.split(',')
    vm.city = vm.city.strip()
    vm.state = vm.state.strip()

    # valid virtual machine data
    vm.valid = True
    return vm
