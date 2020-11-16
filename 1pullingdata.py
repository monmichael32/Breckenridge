import boto3
#from boto3 import dynamodb
from boto3.dynamodb.conditions import Key

def query_info():
   dynamodb = boto3.resource('dynamodb')
   table =  dynamodb.Table('Data')
   r = table.query(
     KeyConditionExpression=Key('Data')#.eq(data)
   )
   return response['Items']

if __name__ ==  '__main__':
    #query_info = data
    data = query_info()
    print(f"Table: {query_info}")
    





#def get_item():
    #dynamodb = boto3.resource('dynamodb')

    #table = dynamodb.Table('Data')

    #r = table.get_item(
        #Key={
            #'id' : 761f9fa5c5a40e5687c970e91d63aef3,
        #}
     #)
    #if 'Item' in r:
        #print(r['Item'][0])


#dynamodb = boto3.client("dynamodb")

#TABLE_NAME = "Data"

# Creating the DynamoDB Client
#dynamodb_client = boto3.client('dynamodb', region_name="us-east-1")

# Creating the DynamoDB Table Resource
#dynamodb = boto3.resource('dynamodb', region_name="us-east-1")


#table = dynamodb.Table('Data')

#response = dynamodb_client.get_item(
    #TableName=Data,
    #Key={
        #'data': {json_object},
    #}
#)
#print(response['Item'])
