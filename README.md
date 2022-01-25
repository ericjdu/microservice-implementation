# CPSC449-Project3

# Members
- Juan Cocina
- Eric Du
- Britney Fernandez

# How to initialize the Databases
- cd into /Project3
- run the command './bin/init.sh'
- Don't CD into bin then try to run the command, it will not work.
- If the folder(s) '/var' or '/var/log' do not exist, the initialization will not work.
In which case, create /Project3/var/log, then retry the command './bin/init.sh'
- Inside /var/log/ there is a file called '.keep'. Its purpose is to keep those two folder when uploaded to github.

# How to run
Using Hug (on the command line)
- 'hug -f timelines.py'
- 'hug -f users.py'

Using foreman (on the command line)
- 'foreman start -m users=1,timelines=3,likes=1,app=1 -p $PORT'
- Replace '$PORT' with you desired port number. I have been using port 8000 for my testing.
- Foreman will then display the ports designated to users and timelines respectively.

# User calls
In browser 
- '/users/' will display all the users in the DB
- '/searchUsers/?username=USERNAME' will search for a username
- '/follows/' will display the USER IDs of who followers who
In the command line
- 'http POST localhost:PORT/createUser/ username=USERNAME email=EMAIL@ADDRESS.COM password=PASSWORD bio=INSERT A BIO'
- The line above will create a user

# Timeline calls
In browser
- '/posts/' displays the public timeline
- '/getUserPosts/?username=USERNAME' will display a specific users' posts
In the command line
- 'http POST localhost:PORT/createPost/ username=USERNAME text=INSERT TEXT HERE'

# Poll Calls
In browser
- '/messages' displays the poll id, user id, message, and options 
In the command line
- to start up DynamoDB, use java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
- to access the list of database(s), aws dynamodb list-tables --endpoint-url http://localhost:8000
- to access the content of the database, aws dynamodb scan --table-name Poll_Table --endpoint-url http://localhost:8000
The file polls_db.py uses boto3 to interact with DynamoDB. The API calls are in app.py. 

If you want to create your own database, follow https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html 

# How to Run Poll Calls Using Hug
- 'hug -f app.py -p 8888'
- Note: you can use any port number

# Like calls
Command Line
- 'http POST localhost:PORT/like/ username=USER_NAME post_id=POST_ID'
- For the post ID, it is a number. The database comes empty, so before attempting the following commands, add posts to the database.
In Browser
- '/likes/user/{username}' will retrieve liked posts_ids from the given user
- '/likes/post/{post_id}' will retrieve which users have liked the given post
- '/popular/' will return the most liked post
- '/likes/post/amount/{post_id}' will return how many likes a post has

# WHAT IS MISSING FROM THE PROJECT
- Service Registry
- Health Checks 
- Updating the posts service to use the service registry

