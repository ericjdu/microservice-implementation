#!/bin/bash

# this section is responsible for creating user.db and user.db tables
sqlite-utils insert ./var/users.db users --csv ./share/users.csv --detect-types --pk=id
sqlite-utils create-index ./var/users.db id username bio email password --unique

sqlite-utils insert ./var/users.db followers --csv ./share/followers.csv --detect-types --pk=id
sqlite-utils create-index ./var/users.db followers id follower_id following_id --unique

# this section is responsible for creating timelines.db and timelines.db tables

sqlite-utils insert ./var/timelines.db timelines --csv ./share/timelines.csv --detect-types --pk=id
sqlite-utils create-index ./var/timelines.db id username text timestamp --unique

