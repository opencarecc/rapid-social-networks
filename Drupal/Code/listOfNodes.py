'''
Returns a list of nodes that were part of the OpenCare study in the legacy Drupal Edgeryders platform.
'''
import csv
import requests

response = requests.get('https://legacy.edgeryders.eu/opencare/content')
posts = response.json()

longList = [] # the accumulator

for node in posts['nodes']:
    item = {}
    item['node_id'] = node['node']['post_id']
    item['title'] = node['node']['title'].encode('utf-8').strip()
    item['user_name'] = node['node']['user_name'].encode('utf-8').strip()
    longList.append(item)


dirPath = '/Users/albertocottica/Downloads/'

with open (dirPath +'opencare_nodes', 'w') as csvfile:
    fieldnames = ['node_id', 'title', 'user_name']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for item in longList:
        writer.writerow(item)
    