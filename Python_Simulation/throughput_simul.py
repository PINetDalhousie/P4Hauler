from lsu_simul import *

import matplotlib.pyplot as plt

files = ["base", "lsu", "prt", "wrr"]


rates = range(100, 1610, 50)

results = {}
for file in files:
	results[file] = {"lat":[], "thg": []}

for name in files:
	file = open(name+".log", "r")
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
	file = open(name + "_128.log", "r")
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
'size' : 10,
}

fig, ax1 = plt.subplots(figsize=(6,2))
ax1.set_ylabel("Throughput (RPS)", font)
ax1.set_xlabel("Rate (RPS)", font)



ax1.plot(rates[8::2], results["base"]["lat"][8::2], marker='.' ,label= "Server-Only 64", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rates[8::2], results["lsu"]["lat"][8::2] , marker='s' ,label= "LSU 64", linestyle="solid", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rates[8::2], results["prt"]["lat"][8::2] , marker='^' ,label= "PRT 64", linestyle="solid", color = "green", mfc="none")  # Plot the chart
ax1.plot(rates[8::2], results["wrr"]["lat"][8::2] , marker='x' ,label= "WRR 64", linestyle="solid", color = "red", mfc="none")  # Plot the chart


# ax1.plot(rates_128[::2], results_128["base"]["lat"][::2], marker='o' ,label= "Server-Only 128", linestyle="--", color = "blue", mfc="none")  # Plot the chart
# ax1.plot(rates_128[::2], results_128["lsu"]["lat"][::2] , marker='P' ,label= "LSU 128", linestyle="--", color = "purple", mfc="none")  # Plot the chart
# ax1.plot(rates_128[::2], results_128["prt"]["lat"][::2] , marker='v' ,label= "PRT 128", linestyle="--", color = "green", mfc="none")  # Plot the chart
# ax1.plot(rates_128[::2], results_128["wrr"]["lat"][::2] , marker='*' ,label= "WRR 128", linestyle="--", color = "red", mfc="none")  # Plot the chart


# ax1.set_ylim(1000, 8000)
ax1.set_xlim(500, 3600)
# ax1.set_yscale('log', basey=2)
plt.yscale('log',base=10) 


# labels = ["1k", "3k", "5k", "7k", "9k" ]
# # plt.xticks(np.arange(1000,9001, 2000), labels)
# plt.xticks(np.arange(1000,9001, 500))

# labels = ["1k", "2k", "4k", "8k"]
# plt.yticks(np.array([1000, 2000, 4000, 8000]), labels)

ax1.legend(ncol=4, fontsize=10, loc="upper left",bbox_to_anchor=(-0.01, 0.52, 1,1))

plt.subplots_adjust(left = 0.1, right=0.99, bottom=0.21, top=0.74)

# # plt.savefig("throughput_1000.pdf")

plt.show()


