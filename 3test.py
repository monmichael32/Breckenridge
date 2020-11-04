import sys, os, base64, datetime, hashlib, hmac 
#from aws_requests_auth.aws_auth import AWSRequestsAuth
import requests

payload = '{"data":"djfgheegejr"}'
method = 'POST'
service = 'execute-api'
host = 'y92lbwe3r2.execute-api.us-east-1.amazonaws.com'
region = 'us-east-1'
endpoint = 'https://y92lbwe3r2.execute-api.us-east-1.amazonaws.com/Production/data'
#request_parameters = 'Action=DescribeRegions&Version=2013-10-15'

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
RoleArn="arn:aws:iam::930811541552:role/Breckenridge"
if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d')

canonical_uri = '/Production/data'
#canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
signed_headers = 'host;x-amz-content-sha256;x-amz-date'
payload_hash = hashlib.sha256((payload).encode('utf-8')).hexdigest()
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-content-sha256:' + payload_hash
#canonical_request = method + '\n' + canonical_uri + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
canonical_request_template = 'POST\n/Production/data\n\nhost:y92lbwe3r2.execute-api.us-east-1.amazonaws.com\nx-amz-content-sha256:PAYLOAD\nx-amz-date:DATEZ\n\nhost;x-amz-content-sha256;x-amz-date\nPAYLOAD'
canonical_request = canonical_request_template.replace('PAYLOAD',payload_hash).replace('DATEZ',amzdate)
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
signing_key = getSignatureKey(secret_key, datestamp, region, service)
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
headers = {'x-amz-date':amzdate,'x-amz-content-sha256':payload_hash, 'Authorization':authorization_header}

request_url = endpoint 


print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = ' + request_url)
r = requests.post(request_url, headers=headers, data=payload)

print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

print("string_to_sign",string_to_sign)

print ("Payload hash: " + payload_hash)


#POST\n/Production/data\n\nhost:y92lbwe3r2.execute-api.us-east-1.amazonaws.com\nx-amz-content-sha256:eca502e47f1e7a14d3bc993d4c8f9e3193822aaa6b78b130d65a882a52a9aab9\nx-amz-date:20201102T225840Z\n\nhost;x-amz-content-sha256;x-amz-date\neca502e47f1e7a14d3bc993d4c8f9e3193822aaa6b78b130d65a882a52a9aab9'


#y92lbwe3r2.execute-api.us-east-1.amazonaws.com

#POST\n/Production/data\n\nhost:y92lbwe3r2.execute-api.us-east-1.amazonaws.com\nx-amz-content-sha256:PAYLOAD\nx-amz-date:DATEZ\n\nhost;x-amz-content-sha256;x-amz-date\nPAYLOAD'
#POST\n/Production/data\n\nhost:y92lbwe3r2.execute-api.us-east-1.amazonaws.com\nx-amz-content-sha256:eca502e47f1e7a14d3bc993d4c8f9e3193822aaa6b78b130d65a882a52a9aab9\nx-amz-date:20201102T230150Z\n\nhost;x-amz-content-sha256;x-amz-date\neca502e47f1e7a14d3bc993d4c8f9e3193822aaa6b78b130d65a882a52a9aab9'
