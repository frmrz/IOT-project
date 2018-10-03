import requests
import json
import time

conf_json=open('conf.json','r').read()
conf_dict=json.loads(conf_json)
payload={
"type": "weight",
"ID": "001",
"users": ["mogetta","cardinali","serrani","marzola"],
"threshold": 0.5
}
i=1
while True:
    r = requests.post(conf_dict['url'], data=json.dumps(payload), headers=conf_dict['headers'])
    print "request %d, content:\n%s" % (i, json.dumps(payload))
    i=i+1
    time.sleep(conf_dict['imalive_time'])
