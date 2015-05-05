import requests
import json
from random import randint

url = "http://10.1.2.55:8888/lamps"
lamps = requests.get(url)

l = {

     "location": {
       "$reql_type$": "GEOMETRY",
       "type": "Point",
       "coordinates": [
         20.315872371653256,
         52.475248828722204
       ]
     },
     "identifier": "Lamp 128",
     "group": [],
     "hardware": {
       "protocol": "madli",
       "building": "stn",
       "is_sensor": False,
       "type": "madli lamp",
       "computer_ip": "10.1.2.55",
       "address": "126"
     },
     "working_l_setting": randint(0, 244),
     "special_l_setting": randint(0, 244),
     "presence_l_setting": randint(0, 244),
     "wanted_l_level": randint(0, 244),
     "actual_driver_value": randint(0, 244),
     "presence_flag": False,
     "special_flag": True,
     "working_flag": True,
     "change_required": True
}



print "Number of lamps in the system is: " + str(len(lamps.json()['response']))

print "Adding next lamp.."
requests.post(url=url,  data=json.dumps(l))
print "Patching existing lamp.."

print "Object was: "
changed_lamp = lamps.json()['response'][0]
another_lamp = lamps.json()['response'][1]
print changed_lamp
changed_lamp['wanted_l_level'] = randint(0, 244)
print "Object now is: "
print changed_lamp

print "patching!"
requests.patch(url=url,  data=json.dumps(changed_lamp))

print "veryfying: "
lamps = requests.get(url)
check_lamp = lamps.json()['response'][0]
print "Object in db is:"
print check_lamp


print "All db: "

ls = lamps.json()['response']
for lu in ls:
    print lu




