import json
import boto3
import uuid
from datetime import datetime

# Connect to the DynamoDB table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Expenses')

def lambda_handler(event, context):
    # Handle CORS preflight request
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
            },
            "body": json.dumps("CORS preflight OK")
        }

    # Handle GET request to fetch expenses
    if event.get("httpMethod") == "GET":
        try:
            response = table.scan()
            items = response.get('Items', [])
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(items)
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": str(e)})
            }

    # Handle POST request to save a new expense
    if event.get("httpMethod") == "POST":
        try:
            body = json.loads(event['body'])
            amount = body.get('amount')
            description = body.get('description')
            timestamp = datetime.utcnow().isoformat()
            expense_id = str(uuid.uuid4())

            # Save to DynamoDB
            table.put_item(Item={
                'id': expense_id,
                'amount': amount,
                'description': description,
                'timestamp': timestamp
            })

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "Expense saved",
                    "id": expense_id
                })
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": str(e)})
            }

    # If request is not GET, POST or OPTIONS
    return {
        "statusCode": 405,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"error": "Method Not Allowed"})
    }
