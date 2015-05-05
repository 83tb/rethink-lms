import requests
import json

url = "http://10.1.2.55:8888/lamps"

lamps = requests.get(url)

print lamps.json()['response'][0]
print lamps.json()['response'][1]


a = lamps.json()['response'][0]
print a

po = requests.post(url=url, data=json.dumps(a))






