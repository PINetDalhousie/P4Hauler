import matplotlib.pyplot as plt
import numpy as np
  
# define data values

def read_from_file(folder_name, rates):
	lat = []
	for i in rates:
		file = open("./" + folder_name+ "/" + str(i)+".log")
		max_p99 = 0
		for line in file:
			line = line.strip().split()
			if len(line) >= 2 and line[0] == "p99:":
				if (float(line[1]) > max_p99): max_p99 = float(line[1])
		lat.append(1000*max_p99)
	return lat


lats = {}
lats["smartnic"] = read_from_file("smartnic", [2000, 4000])
lats["server"] = read_from_file("server", range(2000, 21000, 2000))
lats["switch"] = read_from_file("switch", range(2000, 21000, 2000))

switch_lat = 0.001
# print(lats["smartnic"])
# print(lats["server"])
# print(lats["switch"])


smartnic_lats = [lats["smartnic"][i] - lats["switch"][i] for i in range(2)]
server_lats = [lats["server"][i] - lats["switch"][i] for i in range(10)]
lats["switch"] = [1] * 10
lats["smartnic"] = smartnic_lats
lats["server"] = server_lats
print(lats["server"])
print(lats["switch"])

plt.rcParams.update({
    'font.family': 'Times New Roman',
})

font = {'family' : 'Times New Roman',
	'size' : 10,
}

fig, ax1 = plt.subplots(figsize=(3.5,1.8))

ax1.set_ylabel("P99 Delay (us)", font)
# ax1.set_ylim(0, 10)
ax1.set_xlim(0,9)

ax1.plot(range(2), lats["smartnic"], marker='o' ,label= "SmartNIC-LB", linestyle="--", color = "r", mfc="none")  # Plot the chart
ax1.plot(range(10), lats["server"], marker='x' ,label= "Server-LB", linestyle="-.", color = "b", mfc="none")  # Plot the chart
ax1.plot(range(10), lats["switch"], marker='^' ,label= "Switch-LB", linestyle=":", color = "g", mfc="none")  # Plot the chart

ax1.legend(ncol=3, fontsize=8, bbox_to_anchor=(0.05, 0.38, 0.97,1))
ax1.set_xlabel("Load (KRPS)", font)

labels = ["2", "8", "14", "20"]
plt.xticks(range(0,11,3), labels)
plt.yscale("log")

# plt.yticks([100,1000,10000], [10**2,10**3,10**4])

plt.subplots_adjust(left = 0.15, right=0.97, bottom=0.25, top=0.8)

# plt.savefig("lbs.pdf")
plt.show() 

