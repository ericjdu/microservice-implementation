import configparser
import logging.config
import hug
import sqlite_utils
from datetime import datetime
import requests
import json
import redis

#
# Initializing redis
#
likesDB = redis.Redis(host='localhost', port='6379')

# Route

#
#  gets liked post_ids from a given user
#
@hug.get("/likes/user/{username}")
def getUserLikes(username: hug.types.text):
    results = likesDB.smembers(username)
    if results:
        return results
    else:  # if results is empty
        return {"Status Code": 404, "Message": "Data Not Found"}

#
#  gets which users have liked a specific post
#
@hug.get("/likes/post/{post_id}")
def getPost(post_id: hug.types.number):
    results = likesDB.smembers(post_id)
    if results:
        return results
    else:
        return {"Status Code": 404, "Message": "Data Not Found"}

#
#  gets popular post_id by amount of likes
#
@hug.get("/popular/")
def popularPosts():
    results = likesDB.zrevrange("posts", 0, 0, "withscores")
    if results:
        return results
    else:
        return {"Status Code": 500, "Message": "Contact Administrator"}

#
# gets the amount of likes a post has received
#
@hug.get("/likes/post/amount/{post_id}")
def getLikeAmount(post_id: hug.types.number):
    results = likesDB.zscore("posts", post_id)
    if results:
        return results
    else:
        return {"Status Code": 404, "Message": "Data Not Found"}

#
#  Liking a post (first function made to later test hug.gets
#
@hug.post("/like/",
          example=[
              "username=user_name",
              "post_id=number"
          ])
def likePost(
        response,
        username: hug.types.text,
        post_id: hug.types.number
):
    #  add the user with the post they're liking, added as a set
    likesDB.sadd(username, post_id)
    #  add the post with the user that's liking the post, added as a set
    likesDB.sadd(post_id, username)
    #  count the post likes added a sorted set
    likesDB.zincrby("posts", 1, post_id)

    return {"Like": {"user": username, "post": post_id}}

    
