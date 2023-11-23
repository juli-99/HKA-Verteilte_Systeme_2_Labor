#!/bin/python3

import time
import sys

import zmq

import constMapReduce as const


def cleanText(text: str) -> str:
    return "".join((c.lower() for c in text if c not in ".,?!:;\"'(){}[]|/\\"))

me = int(sys.argv[1])

splitter_address = "tcp://"+ const.SPLITTER_SRC +":"+ const.SPLITTER_PORT

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket
pull_socket.connect(splitter_address)  # connect to splitter 

push_sockets = []
for i in range(const.NUM_REDUCERS):
    reducer_address = "tcp://"+ const.REDUCER_SRC +":"+ str(int(const.REDUCER_PORT)+i)
    push_sockets.append(context.socket(zmq.PUSH)) # create a p push socket
    push_sockets[i].connect(reducer_address) # connect to reducer 

print(f"Mapper {me} started")

while True:
    text = pull_socket.recv_string()  # receive work from a source
    print(f'Mapper {me} received "{text}"')
    words = cleanText(text).split()
    d = {}
    for word in words: 
        if word not in d: 
            d[word] = 1
        else: 
            d[word] += 1

    for k in d: # send to reducer
        reducer = const.HASH(k)
        msg = f"{k}:{d[k]}"
        push_sockets[reducer].send_string(msg)
        print(f"Send {msg} to reducer {reducer}")
    time.sleep(len(d)) # artifical delay

