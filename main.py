# Copyright 2016 Olaf Flebbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import hashlib
import xml.etree.ElementTree

def generate_hash(challenge, password):
    answer = hashlib.md5('{0}-{1}'.format(challenge,password).encode('utf-16le')).hexdigest()
    return '{0}-{1}'.format( challenge, answer)

    str2 = 'username={0}&response={1}-{2}'.format(user,challenge,answer)

def gensid(user, passwd):
    url = 'https://fritz.box/login_sid.lua'
    response = requests.get(url, verify=False)
    e = xml.etree.ElementTree.fromstring(str(response.text))
    for s in e:
        if s.tag == 'Challenge':
            challenge = s.text
            break
    params = { 'username': user, 'response': generate_hash( challenge, passwd)}
    response = requests.get(url, params = params, verify=False)
    e = xml.etree.ElementTree.fromstring(str(response.text))
    print(response.text)
    for s in e:
        if s.tag == 'SID':
            sid = s.text
            break
    if sid == '0000000000000000':
        raise Exception('Mist')
    return sid

def invalidatesid(sid):
    url = 'https://fritz.box/login_sid.lua'
    response = requests.get(url, params = {'sid':sid, 'logout': 1}, verify=False)
    print(response)

sid = gensid('admin','xxx')


def getCall( sid,cmd):
    url = 'https://fritz.box/webservices/homeautoswitch.lua'
    params = { 'sid': sid,  'switchcmd': cmd}
    response = requests.get( url, params = params, verify = False)
    e = xml.etree.ElementTree.fromstring(str(response.text))
    celsius = float(e.find('.//celsius').text)/10.
    power = float(e.find('.//power').text)/1000.
    return power , celsius


power, celsius = getCall(sid,  'getdevicelistinfos')
print (power, celsius)
invalidatesid(sid)

