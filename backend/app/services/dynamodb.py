import boto3
from boto3.dynamodb.conditions import Key, Attr
from schemas.task import TaskResponse
from config.settings import settings
from datetime import datetime, timezone

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
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

def complete_task(task_id):
    response = table.update_item(
        Key={'id': task_id},
        UpdateExpression="set #status=:s",
        ExpressionAttributeValues={
            ':s': 'completed'
        },
        ExpressionAttributeNames={
            '#status': 'status'
        },
        ReturnValues="ALL_NEW"
    )
    return response['Attributes']

def delete_task(task_id):
    table.delete_item(Key={'id': task_id})

def get_overdue_tasks():
    current_date = datetime.now(timezone.utc).isoformat()
    filter_expression = Attr('due_date').lt(current_date) & Attr('notified').eq(False)
    response = table.scan(FilterExpression=filter_expression)
    tasks = [TaskResponse.from_dict(item) for item in response['Items']]
    return tasks