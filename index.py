import boto3
def write(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('counter')
    table.update_item(
    Key={
        'site': 'nathancho.site',
    },
    UpdateExpression='ADD visit :val',
    ExpressionAttributeValues={ ':val': 1 },
    ReturnValues="UPDATED_NEW"
    )
    response = table.get_item(
        Key={
            'site': 'nathancho.site',
        }
    )
    return response['Item']['visit']