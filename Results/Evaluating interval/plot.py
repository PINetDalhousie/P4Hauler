import matplotlib.pyplot as plt
import numpy as np
  
# define data values


def read_results():
	files = ["1-2-0", "2-1-5", "3-1-0", "4-0-5", "5-0-2", "6-0-1", "7-0-05", "8-0-01", "9-0-005"]
	results = []
	for file in files:
		f = open(file+".log", "r")
		for line in f:
			l = line.strip().split()
			if len(l)>0 and l[0] =="p99:":
				results.append(float(l[-1])/1000)
		f.close()
	return results


x = np.array(range(1,10))
lat = read_results()
print(len(lat), len(x))
utl = np.zeros(9)
utl[-1] = 29.1
utl[-2] = 10.5
utl[-3] = 5.6
utl[-4] = 3.5
utl[-5] = 1.9
utl[-6] = 1

print(utl)

plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 10,
}

fig, ax1 = plt.subplots(figsize=(3.5,1.4))

ax1.set_ylabel("P99 Delay (s)", font)
ax1.set_ylim(0, 10)
ax1.set_xlim(2,9)
ax1.plot(x[1:], lat[1:], marker='o' ,label= "99th Delay(s)", linestyle="--", color = "c", mfc="none")  # Plot the chart
ax1.legend(fontsize=8, loc="upper left")
ax1.set_xlabel("Update Rate", font)

ax2 = ax1.twinx()
ax2.set_ylabel("Overhead on CPU (%)", font)
ax2.set_ylim(0,40)
ax2.plot(x[1:], utl[1:], marker='x' ,label= "Overhead (%)", linestyle="--", color = "m", mfc="none")  # Plot the chart
ax2.legend(fontsize=8, loc="upper right")

labels = ["0.5", "0.66", "1", "2", "5", "10", "20", "100", "200"]
plt.xticks(x[1:], labels[1:])


plt.subplots_adjust(left = 0.16, right=0.87, bottom=0.25, top=0.96)

plt.savefig("interval.pdf")
plt.show() 



# plt.figure(figsize=(3.5,2))
# plt.plot(x[1:], lat[1:], marker='o' ,label= "", linestyle="--", color = "k")  # Plot the chart

# # plt.legend()
# # plt.yscale("log")
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("P99 Latency (s)")
# plt.xlim(2,8)



# plt.show()  # display