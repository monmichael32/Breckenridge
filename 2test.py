import sys, os, base64, datetime, hashlib, hmac 
import requests 

method = 'POST'
service = 'lambda'
host = 'lambda.us-east-1.amazonaws.com'
region = 'us-east-1'
#endpoint = 'https://dynamodb.us-east-1.amazonaws.com/'  #endpoint url
endpoint = 'https://lambda.us-east-1.amazonaws.com/'  #endpoint url
endpoint = 'https://y92lbwe3r2.execute-api.us-east-1.amazonaws.com/Production/data'  #endpoint url

#amz_target dynamodb or lambda -where do I find the version. What does it mean operation name
#     DynamoDB_<API version>.<operationName>
content_type = 'application/x-amz-json-1.0'
#amz_target = 'DynamoDB_20120810.CreateTable'
amz_target = 'Lambda_20121017.InvokeFunction'

#Request Params
#request_parameters =  '{'
#request_parameters +=  '"KeySchema": [{"KeyType": "HASH","AttributeName": "Id"}],'
#request_parameters +=  '"TableName": "Data","AttributeDefinitions": [{"AttributeName": "Id","AttributeType": "S"}],'
#request_parameters +=  '"ProvisionedThroughput": {"WriteCapacityUnits": 5,"ReadCapacityUnits": 5}'
#request_parameters +=  '}'

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

#AWS access
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

t = datetime.datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d')

#Canonical Request
canonical_uri = '/'
canonical_querystring = ''
canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n' + 'x-amz-target:' + amz_target + '\n'
signed_headers = 'content-type;host;x-amz-date;x-amz-target'
payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash


#String to sign
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

#Calculate Signature
signing_key = getSignatureKey(secret_key, date_stamp, region, service)
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

#Signing info to the request
  #Auth header
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
headers = {'Content-Type':content_type,
           'X-Amz-Date':amz_date,
           'X-Amz-Target':amz_target,
           'Authorization':authorization_header}

#Sending the request
print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = ' + endpoint)

r = requests.post(endpoint, data=request_parameters, headers=headers)

print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)
print(r)

