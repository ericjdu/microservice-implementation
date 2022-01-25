import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
table = dynamodb.Table('Poll_Table')
print(table)

def load_users():
    user_ids = []
    with open("share/users.csv") as f: 
        users = f.readlines()
        for user in users: 
            if user.startswith("id"):
                continue
            id, _, _, _, _ = user.split(",")
            user_ids.append(id)
    return user_ids


def create_message(poll_id, user_id, message, options, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Poll_Table')
    response = table.put_item(
        Item={
                'PollID': poll_id,
                'user_id': user_id,
                'Message': message,
                'Options': options,
            }
    )
    return response


def get_message(poll_id, user_id, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Poll_Table')
    response = table.get_item(Key={'PollID': poll_id, 'user_id': user_id})
    return response['Item']


def delete_message(poll_id, user_id, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Poll_Table')
    response = table.delete_item(
        Key={
            'PollID': poll_id,
            'user_id': user_id
        }
    ) 


def update_message(poll_id, user_id, message, options, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Poll_Table')

    response = table.update_item(
        Key={
            'PollID': poll_id,
            'user_id': user_id
        },
        UpdateExpression="set Message=:m, Options=:o",
        ExpressionAttributeValues={
            ':m': message,
            ':o': options
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


# if __name__ == '__main__':
#     poll_resp = create_message(1, 1, 'What is your favorite season?', ['Fall', 'Winter', 'Spring', 'Summer'])
#     print("Put Poll succeeded:")

#     poll_resp = create_message(2, 2, 'What is your favorite day of the week?', ['Monday', 'Wednesday', 'Friday', 'Sunday'])
#     print("Put Poll succeeded:")

#     get_message = get_message(2, 2)
#     print("got message")

#     update_mess = update_message(2, 2, 'What is your favorite day?', ['Monday', 'Wednesday', 'Friday', 'Sunday'])
#     print('updated')

#     delete_resp = delete_message(1,1)
#     print("deleted message")
    