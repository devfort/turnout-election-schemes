#!/bin/bash

count="$1"
COUNT=${count:=10}

while [ $COUNT -gt 0 ]; do
  python measure_resource_usage.py 6 100 225; COUNT=$[$COUNT-1]
done | awk 'BEGIN { u = 0; s = 0; r = 0; c = 0 } { u += $2; s += $4; r += $6; c += 1 } END { print "utime", u / c, "stime", s / c, "maxrss", r / c, "across", c, "runs" }'
