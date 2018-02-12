#!/bin/bash


# Get only URL last element of short-listings.txt file
cat short-listings.txt |awk '{print $NF}' |cut -d/ -f5 > junk

# Remove all dashes from file
sed -i -e "s/-/ /g" junk

#
# finds most commond used words
#
tr -c '[:alnum:]' '[\n*]' < junk | sort | uniq -c | sort -nr | head  -20
