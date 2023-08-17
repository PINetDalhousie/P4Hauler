from simulation import *

SERVER = 128
ACCElERATOR = 2

ITERATION = 1000
# LOAD = SERVER * 20

print('baseline:')
for rate in range(1000, 4000, 50):
	lat = np.zeros(SERVER*(ACCElERATOR + 1))
	thg = 0
	for i in range(ITERATION):
		load_base_64, util_base_64, lats_base_64 = baseline(rate,SERVER,ACCElERATOR)
		lat += lats_base_64
		thg += calc_throughput(load_base_64, util_base_64)
	lat /= ITERATION
	thg /= ITERATION
	print(rate, np.percentile(lat,99),  thg)