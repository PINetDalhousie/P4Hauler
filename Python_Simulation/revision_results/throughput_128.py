from simulation import *
import matplotlib.pyplot as plt

import pickle

SERVER = 128
ACCElERATOR = 2

ITERATION = 100
# LOAD = SERVER * 20


T = {"server": [], "lsu": [], "prt": [], "wrr":[]}
L = {"server": [], "lsu": [], "prt": [], "wrr":[]}
rates = range(1600, 3601, 100)


print('baseline:')
for rate in rates:
	lat = np.zeros(SERVER*(ACCElERATOR + 1))
	thg = 0
	for i in range(ITERATION):
		load_base_64, lats_base_64, thrg_base_64 = baseline(rate,SERVER,ACCElERATOR)
		lat += lats_base_64
		thg += calc_throughput(thrg_base_64)
	lat /= ITERATION
	thg /= ITERATION
	# print(rate, np.percentile(lat,99),  thg)
	L["server"].append(np.percentile(lat,99))
	T["server"].append(thg)

print('LSU:')
for rate in rates:
	lat = np.zeros(SERVER*(ACCElERATOR + 1))
	thg = 0
	for i in range(ITERATION):
		load_base_64, lats_base_64, thrg_base_64 = lsu(rate,SERVER,ACCElERATOR)
		lat += lats_base_64
		thg += calc_throughput(thrg_base_64)
	lat /= ITERATION
	thg /= ITERATION
	# print(rate, np.percentile(lat,99),  thg)
	L["lsu"].append(np.percentile(lat,99))
	T["lsu"].append(thg)

print('PRT:')
for rate in rates:
	lat = np.zeros(SERVER*(ACCElERATOR + 1))
	thg = 0
	for i in range(ITERATION):
		load_base_64, lats_base_64, thrg_base_64 = priority(rate,SERVER,ACCElERATOR)
		lat += lats_base_64
		thg += calc_throughput(thrg_base_64)
	lat /= ITERATION
	thg /= ITERATION
	# print(rate, np.percentile(lat,99),  thg)
	L["prt"].append(np.percentile(lat,99))
	T["prt"].append(thg)

print('wrr:')
for rate in rates:
	lat = np.zeros(SERVER*(ACCElERATOR + 1))
	thg = 0
	for i in range(ITERATION):
		load_base_64, lats_base_64, thrg_base_64 = wrr(rate,SERVER,ACCElERATOR)
		lat += lats_base_64
		thg += calc_throughput(thrg_base_64)
	lat /= ITERATION
	thg /= ITERATION
	# print(rate, np.percentile(lat,99),  thg)
	L["wrr"].append(np.percentile(lat,99))
	T["wrr"].append(thg)


with open('128.pkl', 'wb') as file:
	pickle.dump(rates, file)
	pickle.dump(T, file)
	pickle.dump(L, file)