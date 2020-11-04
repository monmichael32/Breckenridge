from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import sys, os, base64, datetime, hashlib, hmac 

#Setting up the webdriver
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
global driver
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

#Signing into the account, and going to the needed URL
driver.get("https://www.bgvgrandcentral.com/")
username = driver.find_element_by_name("loginModel.Username").send_keys("")
Password = driver.find_element_by_name("loginModel.Password").send_keys("")
form = driver.find_element_by_tag_name("form")
form.submit()
driver.get("https://www.bgvgrandcentral.com/reservations/bonus-time")
driver.implicitly_wait(15)
classes = driver.find_element_by_class_name("container")
path_GC8 = '//*[@id="tabGC8"]/a'
path_GL7 = '//*[@id="tabGL7"]/a'
path_GTL = '//*[@id="tabGTL"]/a'
path_GP = '//*[@id="tabGP"]/a'
#list_1 is webelements associated to available dates
list_1 = []
#list_3 refreshed list of webelements after one is clicked on
list_3 = []
myDict = {}

#Selects the lodge via xpath, collects avaialable dates, runs procedure-calls the whole program
def select_lodge(lodge):
  Calendar = []
  myDate = ''
  driver.get("https://www.bgvgrandcentral.com/reservations/bonus-time")
  driver.implicitly_wait(5)
  try:
    driver.implicitly_wait(15)
    driver.find_element_by_xpath(lodge).click()
  except:
    driver.implicitly_wait(30)
    driver.find_element_by_xpath(lodge).click()
  #print(lodge)
  month_dates = get_dates()
  get_date_webelements()
  lodgename = get_lodge_name(lodge)
  print(lodgename)
  print("month_dates:",month_dates)
  Procedure(month_dates,lodge,lodgename)

#Creates a list of the month dates available
def get_dates():
  month_dates = []
  Calendar = driver.find_elements_by_class_name("selectable")
  Date = 0
  for myDate in Calendar: 
    try:
        Calendar = driver.find_elements_by_class_name("selectable")
        D = (myDate.find_element_by_tag_name("a"))
        Date = int(D.text)
        month_dates.extend([Date])
        driver.implicitly_wait(3)
    except:
        pass
  return month_dates

#Collects the webelements connected to the month dates available
def get_date_webelements(): 
  list_1 = []
  Calendar = driver.find_elements_by_class_name("selectable")
  for myDate in Calendar:     
    try:
        Calendar = driver.find_elements_by_class_name("selectable")
        D = (myDate.find_element_by_tag_name("a"))
        list_1.extend([D])
        driver.implicitly_wait(3)
    except:
        pass
  return list_1

#Supplies the lodge name to the dictKey in the dictionary
def get_lodge_name(lodge):
    if lodge == '//*[@id="tabGC8"]/a':
      lodgename = "GC8"
    elif lodge == '//*[@id="tabGL7"]/a':
      lodgename = "GL7"
    elif lodge == '//*[@id="tabGTL"]/a':
      lodgename = "GTL"
    else:
      lodgename = "GP"
    return lodgename

#refreshes the page to deselect previous dates
def refresh(lodge):
    homepage = driver.find_element_by_xpath('//*[@id="topNav"]/div/a/img').click()
    driver.implicitly_wait(10)
    driver.get("https://www.bgvgrandcentral.com/reservations/bonus-time")
    driver.implicitly_wait(5)
    try:
      driver.implicitly_wait(15)
      driver.find_element_by_xpath(lodge).click()
    except:
      driver.implicitly_wait(30)
      driver.find_element_by_xpath(lodge).click()
    driver.implicitly_wait(10)

#Calls the functions to create the dictionary of available dates
def Procedure (month_dates,lodge,lodgename):
  checkout = 0
  indexnumber = 0
  checkin = 0
  list_3 = []
  for Date in month_dates:
    indexnumber = month_dates.index(Date)
    checkout = Date+1
    checkin = str(Date)
    dictKey = (lodgename+"_"+checkin)
    if checkout in month_dates and indexnumber == 0:
      checkinout(indexnumber,Date,dictKey)
      
    elif checkout in month_dates:
      deselect_checkout(indexnumber,Date,lodge,dictKey)
    else:
      checkin_fill(indexnumber,Date,lodge,dictKey)

#Selects intial checkin/out dates
def checkinout (indexnumber,Date,dictKey):
    list_1 = get_date_webelements()
    list_1[indexnumber].click()
    driver.implicitly_wait(3)
    list_3 = (driver.find_elements_by_class_name("selectable"))
    list_3[indexnumber].click() 
    driver.implicitly_wait(3)
    form = driver.find_element_by_tag_name("form")
    form.submit()
    table(myDict,dictKey)
    
#Calls the refresh function and runs checkinout
def deselect_checkout(indexnumber,Date,lodge,dictKey):
    refresh(lodge)
    checkinout(indexnumber,Date,dictKey)

#Selects a single date that auto fills the checkout date          
def checkin_fill(indexnumber,Date,lodge,dictKey):
    refresh(lodge)
    list_1 = get_date_webelements()
    list_1[indexnumber].click()
    driver.implicitly_wait(3)
    form = driver.find_element_by_tag_name("form")
    form.submit()
    driver.implicitly_wait(3)
    table(myDict,dictKey)
    refresh(lodge)

#Populates the dictionary
def table(myDict, dictKey):
    driver.implicitly_wait(3)
    Table = driver.find_elements_by_xpath("/html/body/div[1]/div[5]/div/div[1]/div[2]/div[6]/div/table//tr/td")
    counter = 1
    #lodgeName = dictKey.split('_')[0]
    #dateNum = dictKey.split('_')[1]
    myDict[dictKey] = ""
    for element in Table:
        myDict[dictKey] = myDict[dictKey] + ":" +(element.text)
    dataDict = {}
    dataDict["data"] = myDict
    return dataDict

select_lodge(path_GC8)
select_lodge(path_GL7)
select_lodge(path_GTL)
select_lodge(path_GP)
#converts the dictionary to json
json_object = json.dumps(dataDict, indent = 4)   
print(json_object)
#headers = {'Authorization':'token' '70fy8qsscL27eu5V6TiNS6OMv6SdlEKy2fbGhzni'}
#resp = requests.post('https://y92lbwe3r2.execute-api.us-east-1.amazonaws.com/Production', headers=headers)

#url = 'https://y92lbwe3r2.execute-api.us-east-1.amazonaws.com/Production/data'
#headers = {'Authorization': 'Bearer 123qwe!@#QWE'}
#payload = {'name':'Breckauth', email: 'monmichael32@gmail.com'}

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
if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d')

canonical_uri = '/' 
canonical_querystring = request_parameters
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
signed_headers = 'host;x-amz-date'
payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
signing_key = getSignatureKey(secret_key, datestamp, region, service)
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
headers = {'x-amz-date':amzdate, 'Authorization':authorization_header}

request_url = endpoint + '?' + canonical_querystring


print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = ' + request_url)
r = requests.get(request_url, headers=headers)

print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

#response = requests.post(url, headers=headers, data=payload)
#print (response.status_code)
#print (response.text)
#print (response)
