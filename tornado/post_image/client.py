import argparse
import base64
import sys
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

with open('./lena_gray_256.tif', 'rb') as f:
    rawdata = f.read()

base64_data = base64.b64encode(rawdata).decode('utf-8')
json_data = {'lena_gray_256': base64_data}

if ':' in args.server :
    ip = args.server
else:
    ip = args.server + ':8888'

url = f'http://{ip}'

print(url)

r = requests.post(url, json=json_data)

if r.status_code != 200 :
    print(f'error status code: {r.status_code}')
    sys.exit(1)

print(r.json())

