# Lines 1 - .. will be borrowed from ProfAvery's hug/api
import configparser
import logging.config
import hug
import sqlite_utils
from datetime import datetime
import requests
import json

# Load configuration
config = configparser.ConfigParser()
config.read("./etc/timeline.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# arguments to inject into route functions
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)
#
# authentication
#
@hug.authentication.basic
def context_basic_authentication(username, password, context):
    payload = {
    'username': username,
    'password': password
    }
    response = requests.post('http://localhost:5000/login', data=payload)
    return response.json()

# Gets public timeline
@hug.get("/posts/")
def timelines(db: sqlite):
    return {"timelines": db["timelines"].rows_where(order_by="timestamp desc")}

# Posts onto the timeline
@hug.post("/createPost/", status=hug.falcon.HTTP_201, requires=context_basic_authentication)
def postTweet(
        response,
        username: hug.types.text,
        text: hug.types.text,
        db: sqlite,
):
    timelines = db["timelines"]

    timestamp = datetime.utcnow()
    text = text.replace("%20", " ")
    tweet = {
        "username": username,
        "text": text,
        "timestamp": timestamp,
    }

    try:
        timelines.insert(tweet)
        tweet["id"] = timelines.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"err": str(e)}

    response.set_header("Location", f"/timelines/{tweet['id']}")
    return tweet

#
# Grabs a specific post, using post its post ID
#
@hug.get("/posts/{id}")
def retrieve_post(response, id: hug.types.number, db: sqlite):
    posts = []
    print("test")
    try:
        post = db["timelines"].get(id)
        posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}


#
# search for user tweets/posts/messages (userTimeline)
#
@hug.get(
    "/getUserPosts/",
    example=[
        "username=user_name"
        "text=text"
    ],
)
def getUserPosts(request, db: sqlite, logger:log, requires=context_basic_authentication):
    tweets = db["timelines"]

    conditions = []
    values = []

    if "published" in request.params:
        conditions.append("username = ?")
        values.append(request.params["username"])

    for column in ["username", "text"]:
        if column in request.params:
            conditions.append(f"{column} LIKE ?")
            values.append(f"%{request.params[column]}%")

        if conditions:
            where = " AND ".join(conditions)
            logger.debug('WHERE "%s", %r', where, values)
            return {"timelines": tweets.rows_where(where, values)}
        else:
            return {"timelines": tweets.rows_where(order_by="timestamp desc")}

#
# Home timeline (retrieves posts from users you follow)
#
'''
    At this point, the return from users.py returns the following_ids
    So what do I need to do?
    
    retrieve the posts from all the user ID's,
    return in desc order
    
    the select call would include
'''
@hug.get(
    "/homeTimeline/",
    example=[
        "username=USERNAME"
    ],
)
def homeTimeline(request, db: sqlite, logger: log):
    username = request.params.get("username")

    following_usernames = requests.get(f'http://localhost:8000/userFollows/?username={username}')
    result = following_usernames.json()
    homePosts = []  # list of posts from users that are followed

    for x in result:  # iterate through the result list
        if x['following']: # if username exists, query for their posts, and append
            for column in db.query('SELECT text from timelines where username= ?', [x['following']]):
                homePosts.append(column)
        else:
            return {"Status Code": "404", "Message": "No Posts Could be Found"}

    return homePosts


