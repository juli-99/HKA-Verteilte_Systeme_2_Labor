SPLITTER_SRC = "127.0.0.1"
SPLITTER_PORT = "50000"
REDUCER_SRC = "127.0.0.1"
REDUCER_PORT = "51000"


NUM_REDUCERS = 2

HASH =lambda k: len(k) % NUM_REDUCERS  # "hash" function to determein to whitsch reducer data should be returned (0 to NUM_REDUCERS-1)
