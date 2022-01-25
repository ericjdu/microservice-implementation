from random import random
import hug
import random
import polls_db

@hug.post('/message')
def post_message(user_id, message, options):
    poll_id = random.randint(1, 1000)
    user_ids = polls_db.load_users()
    print(poll_id)
    print(user_ids)
    polls_db.create_message(poll_id, int(user_ids[0]), message, options)

    # response.status = hug.HTTP_200
    return {"Status Code": 200, "Message": "OK", "PollId": poll_id}, 

@hug.get('/message')
def get_message(poll_id, user_id):
    return polls_db.get_message(int(poll_id), int(user_id))

@hug.delete('/message')
def delete_message(poll_id, user_id):
    polls_db.delete_message(int(poll_id), int(user_id))

@hug.patch('/message')
def update_message(poll_id, user_id, message, options):
    return polls_db.update_message(int(poll_id), int(user_id), message, options)
