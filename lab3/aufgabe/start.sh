#!/bin/bash
#
$TERM -e python reducer.py 0 &
$TERM -e python reducer.py 1 &

$TERM -e python mapper.py 0 &
$TERM -e python mapper.py 1 &
$TERM -e python mapper.py 2 &

$TERM -e python splitter.py &

