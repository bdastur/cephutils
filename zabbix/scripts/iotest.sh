#!/bin/bash

outputfile=$1
blocksize=$2

for x in {1..30}
do
    dd if=/dev/zero of=${outputfile} bs=${blocksize}G count=1 oflag=direct
    sleep 1
    rm -f /data/here
    sleep 2
done

