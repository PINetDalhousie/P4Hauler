from lsu_simul import *

import matplotlib.pyplot as plt

files = ["base", "lsu", "prt", "wrr"]


rates = range(100, 1610, 50)

results = {}
for file in files:
	results[file] = {"lat":[], "thg": []}

for name in files:
	file = open("./results/" + name+".log", "r")
	for line in file:
		l = line.strip().split()
		if len(l) == 3:
			l = list(map(float, l))
			results[name]["lat"].append(l[1])
			results[name]["thg"].append(l[2])
	file.close()




rates_128 = range(900, 3650, 50)
results_128 = {}
for file in files:
	results_128[file] = {"lat":[], "thg": []}

for name in files:
	file = open("./results/" + name + "_128.log", "r")
	for line in file:
		l = line.strip().split()
		if len(l) == 3:
			l = list(map(float, l))
			results_128[name]["lat"].append(l[1])
			results_128[name]["thg"].append(l[2])
	file.close()




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
ax1.set_ylabel("Throughput (RPS)", font)
ax1.set_xlabel("Rate (RPS)", font)



ax1.plot(rates[8::2], results["base"]["thg"][8::2], marker='.' ,label= "Server-Only 64", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates[8::2], results["lsu"]["thg"][8::2] , marker='s' ,label= "LSU 64", linestyle="solid", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rates[8::2], results["prt"]["thg"][8::2] , marker='^' ,label= "PRT 64", linestyle="solid", color = "green", mfc="none")  # Plot the chart
ax1.plot(rates[8::2], results["wrr"]["thg"][8::2] , marker='x' ,label= "WRR 64", linestyle="solid", color = "red", mfc="none")  # Plot the chart


ax1.plot(rates_128[6::2], results_128["base"]["thg"][6::2], marker='o' ,label= "Server-Only 128", linestyle="--", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates_128[6::2], results_128["lsu"]["thg"][6::2] , marker='P' ,label= "LSU 128", linestyle="--", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rates_128[6::2], results_128["prt"]["thg"][6::2] , marker='v' ,label= "PRT 128", linestyle="--", color = "green", mfc="none")  # Plot the chart
ax1.plot(rates_128[6::2], results_128["wrr"]["thg"][6::2] , marker='*' ,label= "WRR 128", linestyle="--", color = "red", mfc="none")  # Plot the chart


# ax1.set_ylim(1000, 8000)
ax1.set_xlim(500, 3500)
# # ax1.set_yscale('log', basey=2)
# plt.yscale('log',base=2) 


labels = ["0.5k", "1.0k", "1.5k", "2.0k"]
plt.yticks(np.arange(500,2001, 500), labels, fontsize=11)
# plt.xticks(np.arange(1000,9001, 500))

labels = ["0.5k", "1.0k", "1.5k", "2.0k", "2.5k", "3.0k", "3.5k"]
plt.xticks(np.arange(500,3501, 500), labels, fontsize=11)

ax1.legend(ncol=4, fontsize=10, loc="upper left",bbox_to_anchor=(-0.12, 0.28, 1,1))

plt.subplots_adjust(left = 0.11, right=0.97, bottom=0.15, top=0.82)

plt.savefig("throughput_1000.pdf")

plt.show()


