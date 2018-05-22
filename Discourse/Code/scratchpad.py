import json
with open('/Users/albertocottica/github/local/microfoundations-community-management/data/Edgeryders/Edgesense output/daily.network2.min.json') as json_data:
   d = json.load(json_data)
   
stamps = []
   
for item in d['edges']:
  stamps.append(item['ts'])
  
print min (stamps)
print max (stamps)

periods = 0
for item in d['metrics']:
  periods += 1
  
print periods