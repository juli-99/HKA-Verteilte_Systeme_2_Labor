import multiprocessing as mp

import splitter
import mapper
import reducer

proc_splitter = mp.Process(target=splitter.run)
proc_mapper1 = mp.Process(target=mapper.run)
proc_mapper2 = mp.Process(target=mapper.run)
proc_mapper3 = mp.Process(target=mapper.run)
proc_reducer1 = mp.Process(target=reducer.run, args=(1,))
proc_reducer2 = mp.Process(target=reducer.run, args=(2,))

proc_reducer1.start()
proc_reducer2.start()
proc_mapper1.start()
proc_mapper2.start()
proc_mapper3.start()
proc_splitter.start()

while True:
	x = input()
	if x == "STOP":
		break

proc_splitter.join()
proc_mapper1.kill()
proc_mapper2.kill()
proc_mapper3.kill()
proc_reducer1.kill()
proc_reducer2.kill()
