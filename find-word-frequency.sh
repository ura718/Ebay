#!/bin/bash


# Get only URL last element of short-listings.txt file
cat $1 |awk '{print $NF}' |cut -d/ -f5 > junk

# Remove all dashes from file. The '' after -i is used so sed does not create a backup file.
sed -i '' "s/-/ /g" junk

#
# finds most commond used words
#
tr -c '[:alnum:]' '[\n*]' < junk | sort | uniq -c | sort -nr | head  -20
