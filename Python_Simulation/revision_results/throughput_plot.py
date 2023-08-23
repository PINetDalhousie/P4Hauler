import matplotlib.pyplot as plt

import pickle


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

ax1.plot(rate_64[2:-2], thrg_64["server"][2:-2], marker='o' ,label= "64-Server", linestyle=":", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rate_64[2:-2], thrg_64["lsu"][2:-2], marker='s' ,label= "64-LSU", linestyle=":", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rate_64[2:-2], thrg_64["prt"][2:-2], marker='^' ,label= "64-PRT", linestyle=":", color = "green", mfc="none")  # Plot the chart
ax1.plot(rate_64[2:-2], thrg_64["wrr"][2:-2], marker='x' ,label= "64-WR", linestyle=":", color = "red", mfc="none")  # Plot the chart


ax1.plot(rate_96[5:], thrg_96["server"][5:], marker='.' ,label= "96-Server", linestyle="--", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rate_96[5:], thrg_96["lsu"][5:], marker='P' ,label= "96-LSU", linestyle="--", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rate_96[5:], thrg_96["prt"][5:], marker='v' ,label= "96-PRT", linestyle="--", color = "green", mfc="none")  # Plot the chart
ax1.plot(rate_96[5:], thrg_96["wrr"][5:], marker='X' ,label= "96-WRR", linestyle="--", color = "red", mfc="none")  # Plot the chart

ax1.plot(rate_128[9:-2], thrg_128["server"][9:-2], marker='p' ,label= "128-Server", linestyle="-.", color = "blue", mfc="none")  # Plot the chart
ax1.plot(rate_128[9:-2], thrg_128["lsu"][9:-2], marker='D' ,label= "128-LSU", linestyle="-.", color = "purple", mfc="none")  # Plot the chart
ax1.plot(rate_128[9:-2], thrg_128["prt"][9:-2], marker='<' ,label= "128-PRT", linestyle="-.", color = "green", mfc="none")  # Plot the chart
ax1.plot(rate_128[9:-2], thrg_128["wrr"][9:-2], marker='*' ,label= "128-WRR", linestyle="-.", color = "red", mfc="none")  # Plot the chart

print(rate_64[3], rate_128[-4])

ax1.legend(ncol=3, fontsize=10, loc="upper left",bbox_to_anchor=(-0.12, 0.8, 1,1))
# ax1.legend(ncol=2, fontsize=10, loc="upper right")

ax1.set_xlim(1000,3400)
# ax1.set_ylim(0, 300)


labels = ["1.0k", "1.6k", "2.2k", "2.8k", "3.4k"]
plt.xticks(range(1000,3401,600), labels)

# labels = ["100k", "200k", "300k"]
# plt.yticks(range(100,301,100), labels)

plt.subplots_adjust(left = 0.17, right=0.96, bottom=0.18, top=0.65)

plt.savefig("throughput_simulation.pdf")

plt.show()


