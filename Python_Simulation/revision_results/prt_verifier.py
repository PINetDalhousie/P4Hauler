from simulation import *
import matplotlib.pyplot as plt


SERVER = 1
ACCElERATOR = 1

ITERATION = 2
# LOAD = SERVER * 20


T = {"server": [], "lsu": [], "prt": [], "wrr":[]}
L = {"server": [], "lsu": [], "prt": [], "wrr":[]}

_lats =  {"server": [], "lsu": [], "prt": [], "wrr":[]}

_lats["server"] = 	[160.9097785949707, 176.5733647346496, 190.77907800674444, 261.7897319793701, 323.2439994812012, 444.1322875022891, 667.3306131362915, 1823.5206699371338]
_lats["lsu"] 	=  	[975.175528526306, 	1096.211950778961, 1276.4176082611086, 1708.696398735046, 2138.092811107635, 2635.797469615936, 3028.582956790924, 3953.4584832191463, 4426.733348369598, 5958.2252407073975]
_lats["prt"] 	= 	[186.5355014801025, 181.9323253631591, 188.25536012649536, 250.2061510086059, 335.8019995689391, 653.5560321807963, 1298.826768398285, 2070.9974622726436, 3380.1158261299142, 5283.50367307663]
_lats["wrr"] 	=  	[830.6218767166138, 836.6247010231018, 1034.9562048912048, 838.1338906288147, 1053.207454681396, 1067.003674507141, 1096.479980945587, 1127.4709725379944, 1141.6498160362244, 2793.5623741149902]


_server_avg = 	[185.80069144566855, 173.93492658933005, 177.36393875545926, 213.98200690746307, 238.9820392926534, 292.66244305504694, 444.61884385063536, 1280.4869264364243]
_lsu_avg =  	[624.1208155949911, 623.2144931952158, 700.1274863878886, 828.9389888445536, 941.538393497467, 1091.6652341683705, 1140.3636603128343, 1224.3021587530773, 1417.3171255323623, 1776.6187642071698]
_prt_avg = 		[187.37042744954428, 176.8791933854421, 177.84249915017023, 213.2312446832657, 244.04478788375854, 302.12860041194494, 495.0671258426848, 741.0991922020912, 1161.9275048927025, 1577.259069659956]
_wrr_avg = 		[315.5064543088277, 296.9703058401744, 299.4607620769077, 319.98763879140216, 334.7044603029887, 359.43166547351416, 397.78582936241514, 465.491679807504, 675.1962277624342, 1573.9975702762604]
_thrg = {"server": [], "lsu": [], "prt": [], "wrr":[]}

for i in _server_avg: _thrg["server"].append(3.5*500/i)
for i in _lsu_avg: _thrg["lsu"].append(3.5*500/i)
for i in _prt_avg: _thrg["prt"].append(3.5*500/i)
for i in _wrr_avg: _thrg["wrr"].append(3.5*500/i)


latencies = []
throughputs = []


print('baseline:')
rates = range(2,21,2)
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
	latencies.append(np.percentile(lat,99))
	throughputs.append(thg)

T["prt"] = throughputs
L["prt"] = latencies

latencies = []
throughputs = []


plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 13,
}

fig, ax1 = plt.subplots(figsize=(5,2))
ax1.set_ylabel("Throughput (Bps)", font)
ax1.set_xlabel("Rate (rps)", font)

ax1.plot(rates, T["prt"], marker='.' ,label= "Simulated Throughput", linestyle=":", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates, _thrg["prt"], marker='o' ,label= "Obtained Throughput", linestyle=":", color = "red", mfc="none")  # Plot the chart


ax2 = ax1.twinx()
ax2.set_ylabel("P99 E2E Delay (ms)", font)
ax2.plot(rates, L["prt"], marker='x' ,label= "Simulated E2E Delay", linestyle="-.", color = "tab:blue", mfc="none")  # Plot the chart
ax2.plot(rates, _lats["prt"], marker='s' , label= "Obtained E2E Delay", linestyle="-.", color = "tab:red", mfc="none")  # Plot the chart
ax1.set_xlim(2,20)

# ax1.legend(ncol=4, fontsize=10, loc="upper left",bbox_to_anchor=(-0.12, 0.28, 1,1))
ax1.legend(ncol=1, fontsize=10, bbox_to_anchor=(0.05, 0.6, 0.42,1))
ax2.legend(ncol=1, fontsize=10, bbox_to_anchor=(0.05, 0.6, 0.97,1))
plt.subplots_adjust(left = 0.1, right=0.88, bottom=0.25, top=0.7)

plt.savefig("prt_verify.pdf")

plt.show()


