import requests
import discourse_API_Edgeryders as dapi

api_key = 'b8083582f5016455b50397383374b2acd2fa032dec558efdd8d5efc1c87de180'
key_owner = 'alberto'
dtag = 'ethno-opencare'

call_ann = 'https://edgeryders.eu/administration/annotator/annotations.json?api_key=' + api_key + '&api_username=' + key_owner + '&discourse_tag=' + dtag + '&creator_id=3323&per_page=10000'

call_code = 'https://edgeryders.eu/administration/annotator/codes.json?api_key=' + api_key + '&api_username=' + key_owner + '&per_page=10000'

annotations = requests.get(call_ann).json()
print len(annotations)

codes = requests.get(call_code).json()
print len(codes)


opencare_codes = []
for code in codes:
  if code['id'] not in opencare_codes:
    opencare_codes.append(code['id'])
print len (opencare_codes)

orphan_codes = []
empty_ann = []
for ann in annotations:
  refcode = ann['code_id']
  if refcode == None:
    empty_ann.append(ann)
  elif refcode not in opencare_codes:
    orphan_codes.append(refcode)
print len(empty_ann)
print len (orphan_codes)

print 1445 in opencare_codes