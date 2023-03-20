from simulation import *

SERVER = 128
ACCElERATOR = 2

ITERATION = 1000
# LOAD = SERVER * 20

print('wrr:')
for rate in range(1000, 4000, 50):
	lat = np.zeros(SERVER*(ACCElERATOR + 1))
	thg = 0
	for i in range(ITERATION):
		load_wrr_64, util_wrr_64, lats_wrr_64 = wrr3(rate,SERVER,ACCElERATOR)
		lat += lats_wrr_64
		thg += calc_throughput(load_wrr_64, util_wrr_64)
	# print(util_wrr_64, load_wrr_64)
	lat /= ITERATION
	thg /= ITERATION
	print(rate, np.percentile(lat,99),  thg)


