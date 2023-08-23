from simulation import *
import matplotlib.pyplot as plt


SERVER = 64
ACCElERATOR = 1

ITERATION = 10
# LOAD = SERVER * 20


T = {"server": [], "lsu": [], "prt": [], "wrr":[]}
L = {"server": [], "lsu": [], "prt": [], "wrr":[]}


latencies = []
throughputs = []


print('baseline:')
rates = range(64*2, 64*18, 64)
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
	latencies.append(np.percentile(lat,99))
	throughputs.append(thg)

T["server"] = throughputs
L["server"] = latencies

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

fig, ax1 = plt.subplots(figsize=(5.5,3))
ax1.set_ylabel("Throughput (rps)", font)
ax1.set_xlabel("Rate (rps)", font)

ax1.plot(rates, T["server"], marker='.' ,label= "Server-Only 64", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates, T["server"], marker='.' ,label= "Server-Only 64", linestyle="solid", color = "blue", mfc="none")  # Plot the chart


ax2 = ax1.twinx()
ax2.set_ylabel("P99 E2E Delay (ms)", font)
ax2.plot(rates, L["server"], marker='x' ,label= "Overhead (%)", linestyle="--", color = "m", mfc="none")  # Plot the chart


ax1.legend(ncol=4, fontsize=10, loc="upper left",bbox_to_anchor=(-0.12, 0.28, 1,1))

# plt.subplots_adjust(left = 0.11, right=0.97, bottom=0.16, top=0.82)

# plt.savefig("throughput_1000.pdf")

plt.show()


