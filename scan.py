#!/usr/bin/env python
from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key

def scan_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Data')
    #scan_kwargs = {
        #'FilterExpression': Key('year').between(*year_range),
        #'ProjectionExpression': "#yr, title, info.rating",
        #'ExpressionAttributeNames': {"#yr": "year"}
    #}

    #done = False
    #start_key = None
    #while not done:
    #    if start_key:
    #        scan_kwargs['ExclusiveStartKey'] = start_key
    response = table.scan()
        #display_movies(response.get('Items', []))
        #start_key = response.get('LastEvaluatedKey', None)
        #done = start_key is None
    return response

if __name__ == '__main__':
    def print_movies(movies):
        for movie in movies:
            print(f"\n{movie['year']} : {movie['title']}")
            pprint(movie['info'])

    #query_range = (1950, 1959)
    #print(f"Scanning for movies released from {query_range[0]} to {query_range[1]}...")
    #scan_movies(query_range, print_movies)
    resp = scan_table()
    #print(resp)
    #print()
    myKeys = [sorted(x for x in resp['Items'][0]['data'].keys())]

    #mystring.split("_")[4]

    #print (sorted(resp['Items'][0]['data'].keys()))
    #print ("myKeys:",myKeys)
#for key, value in resp.items():
    #print(key, ' : ', value)
lodges = { 'GC8':[], 'GL7':[], 'GTL':[], 'GP':[]}
for key,value in resp['Items'][0]['data'].items():
    print("---")
    print("Key:",key,)#"Value:",value)
    nights = []
    #room = value.split(":")[5]
    #cost = value.split(":")[6]
    #sleeps = value.split(":")[7]
    #poss = ("    Room Tpye:"+room+" Cost:"+cost+" Sleeps:"+sleeps)
    #print(poss)
    #room2 = value.split(":")[9]
    keys=value.replace(":Room Type:Rate\n(Includes tax & resort fees):Sleeps::","")
    nights=keys.rsplit(":Reserve:")
    date = key
    print("nights:",nights)
    date = [nights]
    
#print (sorted(resp['Items'][0]['data']['GC8_10_13'])
 
for key in resp['Items'][0]['data'].keys():
   newkey = key.split("_")[0]
   #print("newkey:",newkey)
   if (key.split("_")[0] == "GC8"): 
      #print("Key:",key)
      lodges["GC8"].append(key)
   elif (key.split("_")[0] == "GL7"):
      lodges["GL7"].append(key)
   elif key.split("_")[0] == "GTL":
      lodges["GTL"].append(key)
   elif key.split("_")[0] == "GP":
      lodges["GP"].append(key)

print("Lodges:",lodges)
