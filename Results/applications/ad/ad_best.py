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


RATES	= range(400,1001,50)

RESULTS_TYPE = "p99:"

def read_data(r_type):
	results = {}
	for p in list_of_policies: results[p] = []
	for d in list_of_policies:
		for r in RATES:
			file = open("./" + d + "/" + str(r) + ".log", "r")
			p99 = 0
			for line in file:
				l = line.strip().split()
				if len(l)>0 and l[0] == r_type:
					if p99 < float(l[-1]): p99 = float(l[-1])
				elif len(l)>0 and l[0] == "los:" and float(l[-1]) > 2:
					results[d].pop()
			results[d].append(p99)
			file.close()
	return results


results = read_data(RESULTS_TYPE)

RATES	= range(800,2001,100)

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
print(len(results["LSU"]), len(results["PRT"]), len(results["WRR"]))

for i in range(len(results["LSU"])):
	p4hauler.append(min(results["LSU"][i], results["PRT"][i],results["WRR"][i]))

plt.plot(RATES[0:len(results["Server-Only"])], results["Server-Only"], marker='o' ,label= "Server-Only", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
plt.plot(RATES[0:len(results["LSU"])], p4hauler, marker='s' ,label= "P4Hauler", linestyle="solid", color = "tab:red", mfc="none")  # Plot the chart


plt.yscale("log")
plt.xlim(800,2000)
# plt.ylim(90,7500)

plt.tick_params(axis='both', which='major', labelsize=12)
plt.xticks(np.arange(800, 2001, step=400), ["0.8", "1.2", "1.6", "2.0"])

# plt.legend(ncol=2, fontsize=12, bbox_to_anchor=(0.05, 0.404, 1,1))
plt.legend(loc="upper left")

plt.xlabel('Rate (Krps)', font)
plt.ylabel('P99 Latency (ms)', font)
plt.subplots_adjust(left = 0.2, right=0.96, bottom=0.3, top=0.94)

if save_or_show == 0:
	# plt.savefig("../ad_p99_best.pdf")
	plt.show()
else:
	plt.savefig("../ad_p99.pdf")
	# plt.savefig("vgg_p99.pdf", bbox_inches='tight')
