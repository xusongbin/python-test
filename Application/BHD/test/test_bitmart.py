
from urllib import request
from urllib import parse


url = 'https://openapi.bitmart.io/v2/ticker?symbol=LHD_BHD'
resp = request.urlopen(url, timeout=3)
resp = resp.read().decode('utf-8')

print(resp)
