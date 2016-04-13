#!/bin/bash

bench_write_results=$(rados bench 1 --pool benchmark write)

OFS=$IFS
IFS=$'\n'
for LINE in $bench_write_results; do
    bw_grep=$(echo $LINE | grep "Bandwidth (MB/sec)")
    if [[ ! -z $bw_grep ]]; then
        bw_mbps=$(echo $LINE | awk -F " " '{print $3}')
        break
    fi
done

IFS=$OFS
echo $bw_mbps

