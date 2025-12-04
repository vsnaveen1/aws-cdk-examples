# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import json
import logging
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    
    # Log security-relevant request information
    request_context = event.get("requestContext", {})
    identity = request_context.get("identity", {})
    
    logger.info(
        "Request received",
        extra={
            "request_id": context.request_id,
            "source_ip": identity.get("sourceIp"),
            "user_agent": identity.get("userAgent"),
            "table_name": table
        }
    )
    
    if event["body"]:
        item = json.loads(event["body"])
        logger.info(
            "Processing item write",
            extra={
                "item_id": item.get("id"),
                "operation": "put_item"
            }
        )
        year = str(item["year"])
        title = str(item["title"])
        id = str(item["id"])
        dynamodb_client.put_item(
            TableName=table,
            Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
        )
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
    else:
        logger.warning("Request received without payload, using default data")
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "year": {"N": "2012"},
                "title": {"S": "The Amazing Spider-Man 2"},
                "id": {"S": str(uuid.uuid4())},
            },
        )
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
