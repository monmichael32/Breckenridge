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
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

#Signing into the account, and going to the needed URL
driver.get("https://www.bgvgrandcentral.com/")
username = driver.find_element_by_name("loginModel.Username").send_keys("johnnyhughes")
Password = driver.find_element_by_name("loginModel.Password").send_keys("$#REFDVC43refdvc")
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
  green_days = get_dates()
  #data_month = get_month()
  get_date_webelements()
  lodgename = get_lodge_name(lodge)
  print(lodgename)
  print(" green_days:",green_days)
  Procedure(green_days,lodge,lodgename)

#Creates a list of the month dates available
def get_dates():
  green_days = []
  Calendar = driver.find_elements_by_class_name("selectable")
  Date = 0
  for myDate in Calendar: 
    try:
        Calendar = driver.find_elements_by_class_name("selectable")
        D = (myDate.find_element_by_tag_name("a"))
        Date = int(D.text)
        green_days.extend([Date])
        driver.implicitly_wait(3)
    except:
        pass
  return green_days

def get_month(Date):
    month = 0
    Calendar = driver.find_element_by_class_name("selectable")
    #for myDate in Calendar: 
        #try:
            #Calendar = driver.find_elements_by_class_name("selectable")
            #driver.implicitly_wait(3)
    month = Calendar.get_attribute("data-month")
    month = int(month)
            #data_month.extend([month])
    driver.implicitly_wait(3)
        #except:
            #pass
    #return data_month
    return month

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

def is_last_day(Date,month):
    if month == 10 and Date == 30:
        return True
        print ("Last day of the month")
    else:
        return False
   #find attribute data month based on what is currently selected 

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
def Procedure (green_days,lodge,lodgename):
  checkout = 0
  indexnumber = 0
  checkin = 0
  list_3 = []
  for Date in green_days:
    indexnumber = green_days.index(Date)
    checkout = Date + 1
    #print("  CheckinDate:",Date,"Checkout Date:",checkout)
    checkin = str(Date)
    dictKey = (lodgename+"_"+checkin)
    month = get_month(Date)
    if (is_last_day(Date,month)):
      #print("   Month:",month)
      last_day_select(indexnumber,Date,dictKey,lodge)
      #print("   Last day of the month")
    elif checkout in green_days and indexnumber == 0:
      checkinout(indexnumber,Date,dictKey,lodge)
      #print("   Ran first elif")
    elif checkout in green_days:
      deselect_checkout(indexnumber,Date,lodge,dictKey)
      #print("   Ran second elif")
    elif checkout not in green_days:
      #print("   Running checkin_fill")
      checkin_fill(indexnumber,Date,lodge,dictKey)
      
#Selects intial checkin/out dates
def checkinout (indexnumber,Date,dictKey,lodge):
    #print("indexnumber:",indexnumber)
    #refresh(lodge)
    driver.implicitly_wait(3)
    list_1 = get_date_webelements()
    list_1[indexnumber].click()
    driver.implicitly_wait(3)
    list_3 = (driver.find_elements_by_class_name("selectable"))
    #print("   list_3 length:",len(list_3),"Indexnumber:",indexnumber,"Date:",Date)
    list_3[indexnumber].click() 
    driver.implicitly_wait(3)
    form = driver.find_element_by_tag_name("form")
    form.submit()
    table(myDict,dictKey)
    refresh(lodge)
    
#Calls the refresh function and runs checkinout
def deselect_checkout(indexnumber,Date,lodge,dictKey):
    refresh(lodge)
    checkinout(indexnumber,Date,dictKey,lodge)

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
    
def last_day_select(indexnumber,Date,dictKey,lodge):
    refresh(lodge)
    other_month_webelements = []
    list_1 = get_date_webelements()
    list_1[indexnumber].click()
    driver.implicitly_wait(3)
    next_month = driver.find_element_by_css_selector("#datepicker > div > div.ui-datepicker-group.ui-datepicker-group-last > table > tbody > tr:nth-child(1) > td:nth-child(3)")
    #for element in next_month:     
        #try:
    other_month_webelements = (next_month.find_elements_by_tag_name("a"))
            #other_month_webelements.extend([D])
    driver.implicitly_wait(3)
        #except:
                #pass
    #return other_month_webelements
    #print("Other webelements text:",other_month_webelements[0].text)
    other_month_webelements[0].click()
    driver.implicitly_wait(3)
    form = driver.find_element_by_tag_name("form")
    form.submit()
    table(myDict,dictKey)
    refresh(lodge)
    #next_month = driver.find_elements_by_css_selector("#datepicker > div > div.ui-datepicker-group.ui-datepicker-group-last > table > tbody > tr:nth-child(1) > td:nth-child(3)")
    #other_month_webelements = next_month.find_elements_by_tag_name("a")

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
    #return dataDict

select_lodge(path_GC8)
select_lodge(path_GL7)
select_lodge(path_GTL)
select_lodge(path_GP)
#converts the dictionary to json
dataDict = {}
dataDict["data"] = myDict
json_object = json.dumps(dataDict, indent = 4)   
print(json_object)

payload = json_object
#payload='json.dumps({“data”: dataDict})'
#payload = '{"data":"json_object"}'
method = 'POST'
service = 'execute-api'
host = 'y92lbwe3r2.execute-api.us-east-1.amazonaws.com'
region = 'us-east-1'
endpoint = 'https://y92lbwe3r2.execute-api.us-east-1.amazonaws.com/Production/data'

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

