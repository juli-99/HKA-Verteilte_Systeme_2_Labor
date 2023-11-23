import multiprocessing as mp

import pickle
import zmq

import const_address

def run(var, arg):
	address = ""
	if arg == 1:
		address = const_address.REDUCER1
	if arg == 2:
		address = const_address.REDUCER2

	context = zmq.Context()

	pull_socket = context.socket(zmq.PULL)
	pull_socket.bind(address)

	while True:
		word = pickle.loads(pull_socket.recv())

		if word != "":
			var.value += 1
			print("Reducer " + str(arg) + ": count=" + str(var.value) + ", word=" + word)

