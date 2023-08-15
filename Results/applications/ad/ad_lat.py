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

plt.figure(figsize=(3,3))
plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 14,
}

plt.plot(RATES[0:len(results["Server-Only"])], results["Server-Only"], marker='o' ,label= "Server-Only", linestyle="solid", color = "blue", mfc="none")  # Plot the chart
plt.plot(RATES[0:len(results["LSU"])], results["LSU"], marker='s' ,label= "LSU", linestyle="solid", color = "purple", mfc="none")  # Plot the chart
plt.plot(RATES[0:len(results["PRT"])], results["PRT"], marker='^' ,label= "PRT", linestyle="solid", color = "green", mfc="none")  # Plot the chart
plt.plot(RATES[0:len(results["WRR"])], results["WRR"], marker='x' ,label= "WRR", linestyle="solid", color = "red", mfc="none")  # Plot the chart
plt.yscale("log")
plt.xlim(800,2000)
# plt.ylim(90,7500)

plt.tick_params(axis='both', which='major', labelsize=12)
plt.xticks(np.arange(800, 2001, step=400), ["0.8k", "1.2k", "1.6k", "2.0k"])

plt.legend(ncol=2, fontsize=12, bbox_to_anchor=(0.05, 0.404, 1,1))
# plt.legend(fontsize=12)

plt.xlabel('Rate (rps)', font)
plt.ylabel('P99 Delay (ms)', font)
plt.subplots_adjust(left = 0.2, right=0.95, bottom=0.17, top=0.77)
print(results["LSU"])
print((results["Server-Only"][-1] - results["LSU"][-1])/results["Server-Only"][-1])
# plt.show()
# if save_or_show == 0:
	# plt.show()
	# plt.savefig("../ad_p99.pdf")
# else:
	# plt.savefig("../ad_p99.pdf")
	# plt.savefig("vgg_p99.pdf", bbox_inches='tight')
