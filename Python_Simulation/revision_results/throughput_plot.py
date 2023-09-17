import matplotlib.pyplot as plt

import pickle
import numpy as np

with open('64.pkl', 'rb') as file:
	rate_64 = pickle.load(file)
	thrg_64 = pickle.load(file)
	lats_64 = pickle.load(file)


with open('96.pkl', 'rb') as file:
	rate_96 = pickle.load(file)
	thrg_96 = pickle.load(file)
	lats_96 = pickle.load(file)


with open('128.pkl', 'rb') as file:
	rate_128 = pickle.load(file)
	thrg_128 = pickle.load(file)
	lats_128 = pickle.load(file)


with open('256.pkl', 'rb') as file:
	rate_256 = pickle.load(file)
	thrg_256 = pickle.load(file)
	lats_256 = pickle.load(file)

plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 13,
}

fig, ax1 = plt.subplots(figsize=(4,2.5))
ax1.set_ylabel("Throughput (Bps)", font)
ax1.set_xlabel("Rate (rps)", font)

ax1.plot(rate_64[2:-1:2], thrg_64["server"][2:-1:2], marker='o' ,label= "64-Server", linestyle=":", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rate_64[2:-1:2], thrg_64["lsu"][2:-1:2], marker='s' ,label= "64-LUR", linestyle=":", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rate_64[2:-1:2], thrg_64["prt"][2:-1:2], marker='^' ,label= "64-PRT", linestyle=":", color = "green", mfc="none")  # Plot the chart
ax1.plot(rate_64[2:-1:2], thrg_64["wrr"][2:-1:2], marker='x' ,label= "64-WR", linestyle=":", color = "red", mfc="none")  # Plot the chart

ax1.plot(rate_128[4:-1:3], thrg_128["server"][4:-1:3], marker='p' ,label= "128-Server", linestyle="-.", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rate_128[4:-1:3], thrg_128["lsu"][4:-1:3], marker='D' ,label= "128-LUR", linestyle="-.", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rate_128[4:-1:3], thrg_128["prt"][4:-1:3], marker='<' ,label= "128-PRT", linestyle="-.", color = "green", mfc="none")  # Plot the chart
ax1.plot(rate_128[4:-1:3], thrg_128["wrr"][4:-1:3], marker='*' ,label= "128-WRR", linestyle="-.", color = "red", mfc="none")  # Plot the chart


ax1.plot(rate_256[7::4], thrg_256["server"][7::4], marker='.' ,label= "256-Server", linestyle="--", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rate_256[7::4], thrg_256["lsu"][7::4], marker='P' ,label= "256-LUR", linestyle="--", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rate_256[7::4], thrg_256["prt"][7::4], marker='v' ,label= "256-PRT", linestyle="--", color = "green", mfc="none")  # Plot the chart
ax1.plot(rate_256[7::4], thrg_256["wrr"][7::4], marker='X' ,label= "256-WRR", linestyle="--", color = "red", mfc="none")  # Plot the chart


ax1.legend(ncol=3, fontsize=10, loc="upper left",bbox_to_anchor=(-0.12, 0.8, 1,1))
# ax1.legend(ncol=2, fontsize=10, loc="upper right")

ax1.set_yscale('log')
# ax1.set_xscale('log')
ax1.set_xlim(1000,7000)
# ax1.set_ylim(0, 2000)


labels = ["1.0k", "2.0k", "3.0k", "4.0k", "5.0k", "6.0k", "7.0k"]
plt.xticks(range(1000,7001,1000), labels)

# labels = ["100k", "200k", "300k"]
# plt.yticks(range(100,301,100), labels)

plt.subplots_adjust(left = 0.17, right=0.96, bottom=0.18, top=0.65)

plt.savefig("throughput_simulation.pdf")

plt.show()


