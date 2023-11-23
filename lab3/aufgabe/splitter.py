#!/bin/python3

import zmq

import constMapReduce as const

FILE_NAME ="text.txt"

address = "tcp://"+ const.SPLITTER_SRC +":"+ const.SPLITTER_PORT

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket
push_socket.bind(address)  # bind socket to address

print("Splitter started")

with open(FILE_NAME, mode='r') as file:
    for line in file.readlines():
        push_socket.send_string(line)
        print(f'Push "{line}"')

print("Sending file finished")
