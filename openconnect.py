#!/usr/bin/python

import sys
import subprocess
import json

from os.path import expanduser

def openconnect(server, creds, script, protocol):
    if server != '':
        command = ['/usr/local/bin/openconnect', str(server)]
        if script != '':
            command.append('-s')
            command.append(script)
        if protocol != '':
            command.append('--protocol=' + protocol)

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        grep_stdout = p.communicate(input=str(creds))[0]
        print grep_stdout

def parseJson(data):
    config = json.load(data)
    server = ''
    creds = ''
    script = ''
    protocol = ''
    for s in config['servers']:
        if sys.argv[1] == s['name']:
            server = s['server']

            if s.has_key('script'):
                script = s['script']

            if s.has_key('protocol'):
                protocol = s['protocol']

            if s['credentials']['type'] == 'basic':
                for c in s['credentials']['values']:
                    creds = creds + c['username'] + '\n' + c['password'] + '\n'
            elif s['credentials']['type'] == 'stoken':
                p = subprocess.Popen(['stoken'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                creds = s['credentials']['values'][0]['username'] + '\n';
                creds =  creds + p.stdout.read().strip() + '\n';
            break

    return { 'server': server, 'credentials': creds, 'script': script, 'protocol': protocol }

if __name__ == "__main__":
    config_file = expanduser('~') + '/.config/network/openconnect.config'
    if len(sys.argv) > 2:
        config_file = sys.argv[2]

    with open(config_file) as cfh:
        config = parseJson(cfh)
        openconnect(config['server'], config['credentials'], config['script'], config['protocol'])
    
