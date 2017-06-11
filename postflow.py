import json
import requests



action = POST
# path = 'http://192.168.56.101:8181/onos/v1//flows/'
server = '192.168.56.101'
port = '8181'
path = '/onos/v1//flows/'
device1 = 'of:0000000000000001'
device2 = 'of:0000000000000002'
session = requests.Session()
session.auth = ('onos', 'rocks')
data1 = {
    {"priority": 400000,
    "timeout": 0,
    "isPermanent": true,
    "deviceId": "of:0000000000000001",
    "treatment":
    {"instructions": [{"type":"OUTPUT","port":"1"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":2},
    {"type":"ETH_DST","mac":"0E:4A:45:7C:75:C7"},
    {"type":"ETH_SRC","mac":"5E:9D:C5:FF:74:42"}]}},
    {"priority": 400000,
    "timeout": 0,
    "isPermanent": true,
    "deviceId": "of:0000000000000001",
    "treatment":
    {"instructions": [{"type":"OUTPUT","port":"2"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":1},
    {"type":"ETH_DST","mac":"5E:9D:C5:FF:74:42"},
    {"type":"ETH_SRC","mac":"0E:4A:45:7C:75:C7"}]}}
    }

data2 = {
    {"priority": 400000,
    "timeout": 0,
    "isPermanent": true,
    "deviceId": "of:0000000000000002",
    "treatment":
    {"instructions":[{"type":"OUTPUT","port":"1"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":2},
    {"type":"ETH_DST","mac":"5E:9D:C5:FF:74:42"},
    {"type":"ETH_SRC","mac":"0E:4A:45:7C:75:C7"}]}},
    {"priority": 400000,
    "timeout": 0,
    "isPermanent": true,
    "deviceId": "of:0000000000000002",
    "treatment":
    {"instructions":[{"type":"OUTPUT","port":"2"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":1},
    {"type":"ETH_DST","mac":"0E:4A:45:7C:75:C7"},
    {"type":"ETH_SRC","mac":"5E:9D:C5:FF:74:42"}]}}
    }




req1 = requests.Request(action, 'http://%s:%s%s%s' % (server, port, path, device1),
                       data=json.dumps(data1), auth=session.auth)
resp1 = session.send(req1.prepare())
resp1.raise_for_status()

req2 = requests.Request(action, 'http://%s:%s%s%s' % (server, port, path, device2),
                       data=json.dumps(data1), auth=session.auth)
resp2 = session.send(req2.prepare())
resp2.raise_for_status()
