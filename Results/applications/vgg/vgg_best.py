import matplotlib.pyplot as plt
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s',"--save",
                    default=0,
                    dest='save',
                    help='Save or Show (Default show)',
                    type=int
                    )

args = parser.parse_args()
save_or_show = args.save


list_of_policies 	=	["Server-Only", "WRR", "PRT", "LSU"]


RATES	= range(5,75,5)

RESULTS_TYPE = "p99:"

def read_data(r_type):
	results = {}
	for p in list_of_policies: results[p] = []
	for d in list_of_policies:
		for r in RATES:
			file = open("./" + d + "/" + str(r) + ".log", "r")
			for line in file:
				l = line.strip().split()
				if l[0] == r_type:
					results[d].append(float(l[-1]))
				if l[0] == "los:" and float(l[-1]) > 10:
					results[d].pop()
			file.close()
	return results


results = read_data(RESULTS_TYPE)
plt.figure(figsize=(3,1.8))
plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 14,
}

p4hauler = []
# print(len(results["LSU"]), len(results["PRT"]), len(results["WRR"]))
for i in range(len(results["LSU"])):
	p4hauler.append(min(results["LSU"][i], results["PRT"][i],results["WRR"][i]))
plt.plot(RATES[0:len(results["Server-Only"])], results["Server-Only"], marker='o' ,label= "Server-Only", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
plt.plot(RATES[0:len(results["LSU"])], p4hauler, marker='s' ,label= "P4Hauler", linestyle="solid", color = "tab:red", mfc="none")  # Plot the chart
# plt.plot(RATES[0:len(results["PRT"])], results["PRT"], marker='^' ,label= "PRT", linestyle="solid", color = "green", mfc="none")  # Plot the chart
# plt.plot(RATES[0:len(results["WRR"])], results["WRR"], marker='x' ,label= "WRR", linestyle="solid", color = "red", mfc="none")  # Plot the chart
plt.yscale("log")
plt.xlim(10,70)
plt.ylim(90,7500)

plt.tick_params(axis='both', which='major', labelsize=11)
plt.xticks(np.arange(10, 71, step=20))

# plt.legend(ncol=4, fontsize=8, bbox_to_anchor=(0.05, 0.33, 1,1))
# plt.legend(ncol=2, fontsize=12, bbox_to_anchor=(0.05, 0.24, 1,1))
plt.legend()
plt.xlabel('Rate (rps)', font)
plt.ylabel('P99 Latency (ms)', font)
plt.subplots_adjust(left = 0.2, right=0.96, bottom=0.3, top=0.94)

if save_or_show == 0:
	plt.savefig("../vgg_p99_best.pdf")
	plt.show()
else:
	plt.savefig("../vgg_p99.pdf")
	# plt.savefig("vgg_p99.pdf", bbox_inches='tight')
