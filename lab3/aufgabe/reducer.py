#!/bin/python3

import sys

import zmq

import constMapReduce as const


me = int(sys.argv[1])

address = "tcp://"+ const.REDUCER_SRC+":"+ str(int(const.REDUCER_PORT)+me)

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a push socket
pull_socket.bind(address)  # bind socket to address

d = {}

print(f"Reducer {me} started")

while True:
    data = pull_socket.recv_string()
    k,v = data.split(':')
    if k not in d:
        d[k] = int(v)
    else:
        d[k] += int(v)

    print(f'"{k}" accures {d[k]} times.')

