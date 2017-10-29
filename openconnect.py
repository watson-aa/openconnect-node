#!/usr/bin/python

import sys
import subprocess
import json

from os.path import expanduser

def openconnect(server, creds):
    if server != '':
        p = subprocess.Popen(['/usr/local/bin/openconnect', str(server)], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        grep_stdout = p.communicate(input=str(creds))[0]
        print grep_stdout

def parseJson(data):
    config = json.load(data)
    server = ''
    creds = ''
    for s in config['servers']:
        if sys.argv[1] == s['name']:
            server = s['server']
            if s['credentials']['type'] == 'basic':
                for c in s['credentials']['values']:
                    creds = creds + c['username'] + '\n' + c['password'] + '\n'
            elif s['credentials']['type'] == 'stoken':
                p = subprocess.Popen(['stoken'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                creds = s['credentials']['values'][0]['username'] + '\n';
                creds =  creds + p.stdout.read().strip() + '\n';
            break

    return { 'server': server, 'credentials': creds }

if __name__ == "__main__":
    config_file = expanduser('~') + '/.config/network/openconnect.config'
    if len(sys.argv) > 2:
        config_file = sys.argv[2]

    with open(config_file) as cfh:
        config = parseJson(cfh)
        openconnect(config['server'], config['credentials'])
    
