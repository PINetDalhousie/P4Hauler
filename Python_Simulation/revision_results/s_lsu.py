from simulation import *
import matplotlib.pyplot as plt


1

latencies = []
throughputs = []

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
	latencies.append(np.percentile(lat,99))
	throughputs.append(thg)

T["server"] = throughputs
L["server"] = latencies

latencies = []
throughputs = []

print('baseline:')
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
	latencies.append(np.percentile(lat,99))
	throughputs.append(thg)

T["lsu"] = throughputs
L["lsu"] = latencies


latencies = []
throughputs = []

print('baseline:')
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
	latencies.append(np.percentile(lat,99))
	throughputs.append(thg)

T["wrr"] = throughputs
L["wrr"] = latencies



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

ax1.plot(rates, T["server"], marker='.' ,label= "Server-Only", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates, T["lsu"], marker='.' ,label= "LSU 64", linestyle="solid", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rates, T["prt"], marker='.' ,label= "PRT 64", linestyle="solid", color = "green", mfc="none")  # Plot the chart
ax1.plot(rates, T["wrr"], marker='.' ,label= "WRR 64", linestyle="solid", color = "red", mfc="none")  # Plot the chart

# ax2 = ax1.twinx()
# ax2.set_ylabel("P99 E2E Delay (ms)", font)
# ax2.plot(rates, L["server"], marker='x' ,label= "Overhead (%)", linestyle="--", color = "m", mfc="none")  # Plot the chart
# ax2.plot(rates, L["lsu"], marker='x' ,label= "Overhead (%)", linestyle="--", color = "m", mfc="none")  # Plot the chart


# ax1.legend(ncol=4, fontsize=10, loc="upper left",bbox_to_anchor=(-0.12, 0.28, 1,1))
ax1.legend(fontsize=10, loc="upper right")
# plt.subplots_adjust(left = 0.11, right=0.97, bottom=0.16, top=0.82)

# plt.savefig("throughput_1000.pdf")

plt.show()


