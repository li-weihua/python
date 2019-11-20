import argparse
import json
import os
import sys
import hashlib

import requests

parser = argparse.ArgumentParser(description='set server url')

parser.add_argument(
    '-s',
    '--server',
    type=str,
    default='localhost:8888',
    required=False,
    help='set server ip'
    )

args = parser.parse_args()

if ':' in args.server :
    ip = args.server
else:
    ip = args.server + ':8888'

url = f'http://{ip}'
print(f'connectting server url: {url}')

# get md5 hash value of input image
f1 = '../files/lena_gray_256.tif'
f2 = '../files/lena_color_256.tif'

with open(f1, 'rb') as f:
    d1 = f.read()

with open(f2, 'rb') as f:
    d2 = f.read()

h1 = hashlib.md5(d1).hexdigest()
h2 = hashlib.md5(d2).hexdigest()

json_data = {'name': 'lena', 'gender': 'female', 
             'file_hash': {os.path.basename(f1): h1, os.path.basename(f2): h2}
            }


files = {
  'json': json.dumps(json_data),
  os.path.basename(f1): open(f1, 'rb'),
  os.path.basename(f2): open(f2, 'rb'),
}

r = requests.post(url, files=files)

if r.status_code != 200 :
    print(f'error status code: {r.status_code}')
else:
    print(r.json())


