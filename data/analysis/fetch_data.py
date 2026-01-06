import requests
import json



# get events data
data_list = []
for i in range(0,30):
    with requests.get(f'http://127.0.0.1:5000/snotelLogs/masterEvents?sDate={i+1}&eDate={i}') as results:
        data = results.json()
        data_list.extend(data['data'])
        
with open("events.json", "w") as outfile:
    json.dump(data_list, outfile, indent=4) 


#event lookup table
url = "http://127.0.0.1:5000/lookupTables/eventsTable"
with requests.get(url) as results:
    data = results.json()
with open("event_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)     

#goes table lookup table
url = "http://127.0.0.1:5000/lookupTables/goesTable"
with requests.get(url) as results:
    data = results.json()
with open("goes_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)    


#Iridium table lookup table
url = "http://127.0.0.1:5000/lookupTables/iridiumTable"
with requests.get(url) as results:
    data = results.json()
with open("iridium_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)

#master table lookup table
url = "http://127.0.0.1:5000/lookupTables/mastersTable?activeOnly=true"
with requests.get(url) as results:
    data = results.json()
with open("master_telem_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)        


#master table lookup table
url = "http://127.0.0.1:5000/lookupTables/mastersTable?activeOnly=true"
with requests.get(url) as results:
    data = results.json()
with open("master_telem_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4) 

#station lookup table

url = "http://127.0.0.1:5000/lookupTables/stationsTable"
with requests.get(url) as results:
    data = results.json()
with open("station_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4) 