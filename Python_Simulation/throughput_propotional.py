# from lsu_simul import *

import matplotlib.pyplot as plt
import numpy as np

files = ["base", "lsu", "prt", "wrr"]


rates = range(100, 1760, 50)

results = {}
for file in files:
	results[file] = {"lat":[], "thg": []}

for name in files:
	file = open("./results/" + name+"_64.log", "r")
	for line in file:
		l = line.strip().split()
		if len(l) == 3:
			l = list(map(float, l))
			results[name]["lat"].append(l[1])
			results[name]["thg"].append(l[2])
	file.close()




rates_128 = range(1000, 4000, 50)
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



for i in range(len(rates)):
	results["base"]["thg"][i] /= rates[i]
	results["lsu"]["thg"][i] /= rates[i]
	results["prt"]["thg"][i] /= rates[i]
	results["wrr"]["thg"][i] /= rates[i]


for i in range(len(rates_128)):
	results_128["base"]["thg"][i] /= rates_128[i]
	results_128["lsu"]["thg"][i] /= rates_128[i]
	results_128["prt"]["thg"][i] /= rates_128[i]
	results_128["wrr"]["thg"][i] /= rates_128[i]


plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 10,
}

fig, ax1 = plt.subplots(figsize=(4,2))
ax1.set_ylabel("Percentage of\nProcessed Requests (%)", font)
ax1.set_xlabel("Rate (RPS)", font)


ax1.plot(rates[8:22:2], results["base"]["thg"][8:22:2], marker='.' ,label= "Server-Only 64", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates[8:26:2], results["lsu"]["thg"][8:26:2] , marker='s' ,label= "LSU 64", linestyle="solid", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rates[8:32:2], results["prt"]["thg"][8:32:2] , marker='^' ,label= "PRT 64", linestyle="solid", color = "green", mfc="none")  # Plot the chart
ax1.plot(rates[8:32:2], results["wrr"]["thg"][8:32:2] , marker='x' ,label= "WRR 64", linestyle="solid", color = "red", mfc="none")  # Plot the chart

ax1.plot(rates_128[6:22:2], results_128["base"]["thg"][6:22:2], marker='o' ,label= "Server-Only 128", linestyle="--", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates_128[6:32:2], results_128["lsu"]["thg"][6:32:2] , marker='P' ,label= "LSU 128", linestyle="--", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rates_128[6::2], results_128["prt"]["thg"][6::2] , marker='v' ,label= "PRT 128", linestyle="--", color = "green", mfc="none")  # Plot the chart
ax1.plot(rates_128[6::2], results_128["wrr"]["thg"][6::2] , marker='*' ,label= "WRR 128", linestyle="--", color = "red", mfc="none")  # Plot the chart


ax1.set_ylim(0.6, 1)
plt.yticks(np.arange(0.6, 1.1, step=0.2))


ax1.set_xlim(500, 3000)



# labels = ["1k", "3k", "5k", "7k", "9k" ]
# plt.xticks(np.arange(1000,9001, 2000), labels)

labels = ["0.5k", "1.0k", "1.5k", "2.0k", "2.5k", "3.0k"]
plt.xticks(np.arange(500,3001, 500), labels)


ax1.legend(ncol=2, fontsize=10, loc="upper left",bbox_to_anchor=(0, 1.4, 1,1))

plt.subplots_adjust(left = 0.16, right=0.96, bottom=0.2, top=0.55)

plt.savefig("throughput_1000_p.pdf")
plt.show()

