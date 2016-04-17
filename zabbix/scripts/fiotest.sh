#!/bin/bash

outputfile=$1
filesize=$2


# FIO Write test.

fio --name=writefile --size=2G --filesize=${filesize}G --filename=$outputfile --bs=1M \
      --nrfiles=1 --direct=1 --sync=0 --randrepeat=0 --rw=write --refill_buffers --end_fsync=1 \
        --iodepth=200 --ioengine=libaio

