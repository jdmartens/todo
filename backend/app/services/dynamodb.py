import boto3
from boto3.dynamodb.conditions import Key
from config.settings import aws_config

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_config.aws_access_key_id,
    aws_secret_access_key=aws_config.aws_secret_access_key,
    region_name=aws_config.region_name
)
table = dynamodb.Table('TodoTasks')

def table_exists(table_name):
    try:
        dynamodb.Table(table_name).load()
        return True
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        return False

def create_table(table_name):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()
    return table


def get_all_tasks(status: str = "pending"):
    filter_expression = Key('status').eq(status)
    response = table.scan(FilterExpression=filter_expression)
    return response['Items']

def get_task(id: str):
    response = table.get_item(Key={'id': id})
    return response['Item']

def add_task(task):
    print("new task", task)
    table.put_item(Item=task.to_dict())

def update_task(task_id, task_data):
    response = table.update_item(
        Key={'id': task_id},
        UpdateExpression="set task_name=:n, due_date=:d, #type=:t",
        ExpressionAttributeValues={
            ':n': task_data.task_name,
            ':d': task_data.due_date.isoformat(),
            ':t': task_data.type
        },
        ExpressionAttributeNames={
            '#type': 'type'
        },
        ReturnValues="ALL_NEW"
    )
    return response['Attributes']

def delete_task(task_id):
    table.delete_item(Key={'id': task_id})
