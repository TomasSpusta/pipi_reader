import json
import requests
  
payload = {"rfid":"912853855591"}
response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)

data = response.json()


#print (data)
#print (type(data))
#print (data[0]["firstname"] + " " + data[0]["lastname"] )
#print (data[0]["full_name"])
