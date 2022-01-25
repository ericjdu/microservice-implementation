#!/bin/bash

sqlite-utils insert ./var/timelines.db timelines --csv ./share/timelines.csv --detect-types --pk=id
sqlite-utils create-index ./var/timelines.db id username text timestamp --unique