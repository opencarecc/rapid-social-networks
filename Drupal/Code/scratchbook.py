import requests

call = 'https://edgeryders.eu/t/6540.json?include_raw=1'
response = requests.get(call)
top = response.json()
onePost = top['post_stream']['posts'][2]
