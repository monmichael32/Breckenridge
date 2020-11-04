#!/usr/bin/env python
import requests
#from date import strftime
import sys, os, base64, datetime, hashlib, hmac

#params = {'Unicorn': 'Butts'}
data = {"Ithinkthey": "fartRainbows"}

#headers = {}
#headers["Authorization"] = "Bearer 70fy8qsscL27eu5V6TiNS6OMv6SdlEKy2fbGhzni"
#authorization_header = "70fy8qsscL27eu5V6TiNS6OMv6SdlEKy2fbGhzni"

#content_type = 'application/x-amz-json-1.0'
#t = datetime.datetime.utcnow()
#amz_date = datetime.date.strftime(t, '%Y%m%dT%H%M%SZ')    #.strftime('%Y%m%dT%H%M%SZ')  
#amz_target = 'Lambda_20121017.InvokeFunction'

#headers = {'Content-Type':content_type,
#           'X-Amz-Date':amz_date,
#           'X-Amz-Target':amz_target,
#           'Authorization':authorization_header}
#resp = requests.post('https://y92lbwe3r2.execute-api.us-east-1.amazonaws.com/Production', params=None, data=data, headers=headers)
resp = requests.post('https://y92lbwe3r2.execute-api.us-east-1.amazonaws.com/Production/Data', data=data)

print (resp.status_code)
print (resp.text)
print (resp)
