import json
import requests



action = 'POST'
# path = 'http://192.168.56.101:8181/onos/v1/flows/'
server = '192.168.56.101'
port = '8181'
path = '/onos/v1/flows/'
device1 = 'of:0000000000000001'
device2 = 'of:0000000000000002'
session = requests.Session()
session.auth = ('onos', 'rocks')
datas = []
data = {
    "priority": 10,
    "timeout": 0,
    "isPermanent": True,
    "deviceId": "of:0000000000000001",
    "treatment":
    {"instructions": [{"type":"OUTPUT","port":"3"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":1},
    {"type":"ETH_DST","mac":"00:00:00:00:00:02"},
    {"type":"ETH_SRC","mac":"00:00:00:00:00:01"}]}}
datas.append(data)
data = {
    "priority": 10,
    "timeout": 0,
    "isPermanent": True,
    "deviceId": "of:0000000000000001",
    "treatment":
    {"instructions": [{"type":"OUTPUT","port":"1"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":2},
    {"type":"ETH_DST","mac":"00:00:00:00:00:01"},
    {"type":"ETH_SRC","mac":"00:00:00:00:00:02"}]}}
datas.append(data)
data = {
    "priority": 10,
    "timeout": 0,
    "isPermanent": True,
    "deviceId": "of:0000000000000002",
    "treatment":
    {"instructions":[{"type":"OUTPUT","port":"2"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":1},
    {"type":"ETH_DST","mac":"00:00:00:00:00:01"},
    {"type":"ETH_SRC","mac":"00:00:00:00:00:02"}]}}
datas.append(data)
data = {
    "priority": 10,
    "timeout": 0,
    "isPermanent": True,
    "deviceId": "of:0000000000000002",
    "treatment":
    {"instructions":[{"type":"OUTPUT","port":"1"}]},
    "selector":
    {"criteria":[{"type":"IN_PORT","port":3},
    {"type":"ETH_DST","mac":"00:00:00:00:00:02"},
    {"type":"ETH_SRC","mac":"00:00:00:00:00:01"}]}}
datas.append(data)


for data in datas:
	req = requests.Request(action, 'http://%s:%s%s%s' % (server, port, path, data["deviceId"]),
                       data=json.dumps(data), auth=session.auth)
	resp = session.send(req.prepare())
	resp.raise_for_status()

