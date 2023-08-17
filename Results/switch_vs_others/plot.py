import matplotlib.pyplot as plt
import numpy as np
  
# define data values

def read_from_file(folder_name, rates):
	lat = []
	for i in rates:
		file = open("./" + folder_name+ "/" + str(i)+".log")
		for line in file:
			line = line.strip().split()
			if len(line) >= 2 and line[0] == "p99:":
				lat.append(float(line[1]))
	return lat


lats = {}
lats["smartnic"] = read_from_file("smartnic", range(100,501,100))
lats["server"] = read_from_file("server", [100,200,300,400,500,1000,1500,2000,2500,3000,3500,4000])
lats["switch"] = read_from_file("switch", [100,200,300,400,500,1000,1500,2000,2500,3000,3500,4000])


# print(lats["smartnic"])
# print(len(lats["server"]))
print(lats["switch"], len(lats["switch"]))

plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 10,
}

fig, ax1 = plt.subplots(figsize=(3,1.5))

ax1.set_ylabel("P99 Delay (ms)", font)
ax1.set_ylim(0, 22)
ax1.set_xlim(1,12)
ax1.plot(range(1,6), lats["smartnic"], marker='o' ,label= "SmartNIC-LB", linestyle="--", color = "r", mfc="none")  # Plot the chart
ax1.plot(range(1,13), lats["server"], marker='x' ,label= "Server-LB", linestyle="-.", color = "b", mfc="none")  # Plot the chart
ax1.plot(range(1,13), lats["switch"], marker='^' ,label= "Switch-LB", linestyle=":", color = "g", mfc="none")  # Plot the chart


ax1.legend(fontsize=8, loc="upper right")
ax1.set_xlabel("Load (KRPS)", font)

labels = ["1", "2", "3", "4", "5", "10", "20", "30", "40"]
plt.xticks([1,2,3,4,5,6,8,10,12], labels)




plt.subplots_adjust(left = 0.16, right=0.97, bottom=0.28, top=0.96)

plt.savefig("lbs.pdf")
plt.show() 

