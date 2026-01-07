import requests
import json



# get events data
data_list = []
for i in range(0,31):
    with requests.get(f'http://127.0.0.1:5000/snotelLogs/masterEvents?sDate={i+1}&eDate={i}') as results:
        data = results.json()
        data_list.extend(data['data'])
        
with open("./data/events.json", "w") as outfile:
    json.dump(data_list, outfile, indent=4) 


#event lookup table
url = "http://127.0.0.1:5000/lookupTables/eventsTable"
with requests.get(url) as results:
    data = results.json()
with open("./data/event_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)     

#goes table lookup table
url = "http://127.0.0.1:5000/lookupTables/goesTable"
with requests.get(url) as results:
    data = results.json()
with open("./data/goes_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)    


#Iridium table lookup table
url = "http://127.0.0.1:5000/lookupTables/iridiumTable"
with requests.get(url) as results:
    data = results.json()
with open("./data/iridium_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)

#master table lookup table
url = "http://127.0.0.1:5000/lookupTables/mastersTable?activeOnly=true"
with requests.get(url) as results:
    data = results.json()
with open("./data/master_telem_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4)        


#master table lookup table
url = "http://127.0.0.1:5000/lookupTables/mastersTable?activeOnly=true"
with requests.get(url) as results:
    data = results.json()
with open("./data/master_telem_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4) 

#station lookup table

url = "http://127.0.0.1:5000/lookupTables/stationsTable"
with requests.get(url) as results:
    data = results.json()
with open("./data/station_lut.json", "w") as outfile:
    json.dump(data, outfile, indent=4) 