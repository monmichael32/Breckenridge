#!/usr/bin/env python
from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key

def scan_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Data')
    response = table.scan()
    return response

if __name__ == '__main__':
            resp = scan_table()
    	    #print(resp)
    	    #print()
            myKeys = [sorted(x for x in resp['Items'][0]['data'].keys())]

def Creating_date_list(key,value):
    nights = []
    keys=value.replace(":Room Type:Rate\n(Includes tax & resort fees):Sleeps::","")
    nights=keys.rsplit(":Reserve:")
    print("   nights:",nights)
    return nights

nights = []
lodges = { 'GC8':[], 'GL7':[], 'GTL':[], 'GP':[]}
for key,value in resp['Items'][0]['data'].items():
    print("---")
    print("Key:",key,)#"Value:",value)
    #Creating_data_list(key,value)
    #keys=value.replace(":Room Type:Rate\n(Includes tax & resort fees):Sleeps::","")
    #nights=keys.rsplit(":Reserve:")
    #print("date=key:",date)
    date = key
    #date = [nights]
    #print("  date=nights ",date)
    #print("   nights:",nights)
    #nights[key].append(keyss)
    if (key.split("_")[0] == "GC8"):
      #print("Key:",key)
      nights = Creating_date_list(key,value)
      lodges["GC8"].append( {key:nights} )
      #Creating_date_list(key,value)
    elif (key.split("_")[0] == "GL7"):
      nights = Creating_date_list(key,value)
      lodges["GL7"].append( {key:nights} )
    elif key.split("_")[0] == "GTL":
      Creating_date_list(key,value)
      lodges["GTL"].append( {key:nights} )
    elif key.split("_")[0] == "GP":
      Creating_date_list(key,value)
      lodges["GP"].append( {key:nights} )
print("Lodges:",lodges)
