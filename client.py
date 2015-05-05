import requests
import json

url = "http://10.1.2.55:8888/lamps"

lamps = requests.get(url)


a = lamps.json()['response'][1]
print a
print len(lamps.json()['response'])


po = requests.post(url=url, data=json.dumps(a))






