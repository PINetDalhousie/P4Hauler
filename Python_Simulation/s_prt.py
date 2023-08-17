from simulation import *

SERVER = 128
ACCElERATOR = 2

ITERATION = 1000
# LOAD = SERVER * 20

print('prt:')
for rate in range(1000, 4000, 50):
	lat = np.zeros(SERVER*(ACCElERATOR + 1))
	thg = 0
	for i in range(ITERATION):
		load_prt_64, util_prt_64, lats_prt_64 = priority(rate,SERVER,ACCElERATOR)
		lat += lats_prt_64
		thg += calc_throughput(load_prt_64, util_prt_64)
	# print(util_prt_64, load_prt_64)
	lat /= ITERATION
	thg /= ITERATION
	print(rate, np.percentile(lat,99),  thg)