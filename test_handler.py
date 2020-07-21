import boto3
import pytest
from moto import mock_dynamodb2
from index import write
from decimal import Decimal

# Test Setup Functions

from contextlib import contextmanager

@contextmanager
def do_test_setup():
    with mock_dynamodb2():
        set_up_dynamodb()
        yield

def set_up_dynamodb():
    client = boto3.client('dynamodb', region_name='us-east-1')
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'site',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'site',
                'KeyType': 'HASH'
            }
        ],
        TableName='counter',
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

# Tests

def test_ddb():
    with do_test_setup():
        write(event, None)
        table = boto3.resource('dynamodb', region_name='us-east-1').Table('counter')
        item = table.get_item(Key={'site': 'nathancho.site'})['Item']
        assert item['visit'] == Decimal(1)

# Helpers
def event():
    {
        "key1": "value1",
    }
