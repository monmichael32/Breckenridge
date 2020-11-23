#!/usr/bin/env python
from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key
from operator import itemgetter

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
    #print("   nights:",nights)
    return nights
print("---")
nights = []
lodges = { 'GC8':[], 'GL7':[], 'GTL':[], 'GP':[]}
for key,value in resp['Items'][0]['data'].items():
    #print("---")
    #print("Key:",key,)#"Value:",value)
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
print("---")

Dates = []
def structuring_based_on_date(lodges):
    #newlodges = [(x for x in lodges['lodges'].keys())]
    #lodge_keys = (lodges.keys)
    #print("   lodge_keys:",lodge_keys)
    for lodge in lodges.keys():
        #newlodges = [(x for x in lodges['lodge'].keys())]
        #print ("   Newlodges:", lodges['Items'][0]['data'][lodge])
        #print("   Lodge:",lodges[lodge]) 
        dateLists = lodges[lodge]
        print("    dateLists:",dateLists)
        for lodgeDateDict in dateLists:
            for lodgeDate in lodgeDateDict.keys():
               date = lodgeDate.lstrip("GC8TLP7")
               date = date.replace("_","")
               print("lodge:",lodge,"   Date: ",date)
               print(lodgeDateDict[lodgeDate])
               if date in Dates:                  
                  print("   In List")
                  Dates[Room].update(lodgeDateDict[lodgeDate])
               elif date not in Dates:
                  print("   Not in List")
                  Dates.append( date = ({"date":date,"Room":lodgeDateDict[lodgeDate]}) )
               #f = itemgetter(date)
               #Dates.sort(key=f)
        print("---")
        print("Dates: ",Dates)
        #f = itemgetter(date)
        #Dates.sort(key=f)
        Dates.sort(key=lambda item: item.get("date"))
structuring_based_on_date(lodges)
print("---")
print("   Dates:",Dates)
#print("   Dates:",sorted(Dates))
print("---")
