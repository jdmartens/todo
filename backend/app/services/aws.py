import boto3
from botocore.exceptions import ClientError
from config.settings import settings

class SESService:
    def __init__(self):
        self.client = boto3.client(
            'ses', 
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.from_email = settings.SES_FROM_EMAIL
        self.to_email = settings.SES_TO_EMAIL

    def send_task_email(self, task):
        subject = f"Task Update: {task.task_name}"
        body_html = f"""
        <html>
        <body>
            <h2>Task Details:</h2>
            <p><strong>Name:</strong> {task.task_name}</p>
            <p><strong>Due Date:</strong> {task.due_date}</p>
            <p><strong>Status:</strong> {task.status}</p>
        </body>
        </html>
        """

        try:
            response = self.client.send_email(
                Source=self.from_email,
                Destination={'ToAddresses': [self.to_email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Html': {'Data': body_html}}
                }
            )
        except ClientError as e:
            print(f"An error occurred: {e.response['Error']['Message']}")
            return False
        else:
            print(f"Email sent! Message ID: {response['MessageId']}")
            return True