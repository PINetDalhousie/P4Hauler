from simulation import *

SERVER = 64
ACCElERATOR = 1


LOAD = SERVER * 20

# lat = np.zeros(SERVER*(ACCElERATOR + 1))
# thg = 0
# for i in range(100):
# 	load_base_64, util_base_64, lats_base_64 = baseline(LOAD,SERVER,ACCElERATOR)
# 	lat += lats_base_64
# 	thg += calc_throughput(load_base_64, util_base_64)
# lat /= 100
# thg /= 100
# print("base: ")
# print("latency:\t", np.percentile(lat,99))
# print("Throughput:\t", thg, LOAD)
# print("\\\\\\\\\\\\\n")


# lat = np.zeros(SERVER*(ACCElERATOR + 1))
# thg = 0
# for i in range(100):
# 	load_lsu_64, util_lsu_64, lats_lsu_64 = lsu(LOAD,SERVER,ACCElERATOR)
# 	lat += lats_lsu_64
# 	thg += calc_throughput(load_lsu_64, util_lsu_64)
# lat /= 100
# thg /= 100
# # print(util_lsu_64)
# # print(lats_lsu_64)
# print("LSU: ")
# print("latency:\t", np.percentile(lat,99))
# print("Throughput:\t", thg, LOAD)
# print("\\\\\\\\\\\\\n")


lat = np.zeros(SERVER*(ACCElERATOR + 1))
thg = 0
for i in range(1000):
	load_prt_64, util_prt_64, lats_prt_64 = priority(LOAD,SERVER,ACCElERATOR)
	lat += lats_prt_64
	thg += calc_throughput(load_prt_64, util_prt_64)
lat /= 1000
thg /= 1000

print("PRT: ")
print(util_prt_64, load_prt_64)
print("latency:\t", np.percentile(lat,99))
print("Throughput:\t", thg, LOAD)


print("\\\\\\\\\\\\\n")


lat = np.zeros(SERVER*(ACCElERATOR + 1))
thg = 0
for i in range(1000):
	load_wrr_64, util_wrr_64, lats_wrr_64 = wrr(LOAD,SERVER,ACCElERATOR)
	lat += lats_wrr_64
	thg += calc_throughput(load_wrr_64, util_wrr_64)
lat /= 1000
thg /= 1000

print("WRR: ")
print(util_wrr_64, load_wrr_64)
print(lats_wrr_64)
print("latency:\t", np.percentile(lat,99))
print("Throughput:\t", thg, LOAD)



