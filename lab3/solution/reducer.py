import multiprocessing as mp

import pickle
import zmq

import const_address

def run(arg):
	address = ""
	if arg == 1:
		address = const_address.REDUCER1
	if arg == 2:
		address = const_address.REDUCER2

	context = zmq.Context()

	pull_socket = context.socket(zmq.PULL)
	pull_socket.bind(address)

	word_counts = {}

	while True:
		word = pickle.loads(pull_socket.recv())

		if word != "":
			if not word in word_counts:
				word_counts[word] = 0
			
			word_counts[word] += 1

			print("reducer " + str(arg) + ": count=" + str(word_counts[word]) + ", word=" + word)
