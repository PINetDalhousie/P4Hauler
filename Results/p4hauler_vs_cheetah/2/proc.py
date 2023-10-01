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


list_of_policies 	=	["p4hauler", "cheetah"]


RATES	= range(20,41,2)

RESULTS_TYPE = "p99:"

def read_data(r_type):
	results = {}
	for p in list_of_policies: results[p] = []
	for d in list_of_policies:
		for r in RATES:
			file = open("./" + d + "/" + str(r) + ".log", "r")
			s = 0
			for line in file:
				l = line.strip().split()
				if len(l) > 0 and l[0] == r_type:
					s += float(l[-1])

			results[d].append(s/10000)
			file.close()
	return results


results = read_data(RESULTS_TYPE)
plt.figure(figsize=(3,1.3))
plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 10,
}

print(results["p4hauler"])
print(results["cheetah"])
plt.plot(RATES, results["p4hauler"], marker='x' ,label= "P4Hauler", linestyle="--", color = "tab:red", mfc="none")  # Plot the chart
plt.plot(RATES, results["cheetah"], marker='o' ,label= "Cheetah", linestyle="-.", color = "tab:blue", mfc="none")  # Plot the chart

# plt.yscale("log")
plt.xlim(20,40)
plt.ylim(0,5)

plt.tick_params(axis='both', which='major', labelsize=9)
plt.xticks(np.arange(20, 41, step=4))

plt.yticks(np.arange(1, 6, step=2))


# plt.legend(ncol=4, fontsize=8, bbox_to_anchor=(0.05, 0.33, 1,1))
# plt.legend(ncol=2, fontsize=8, bbox_to_anchor=(0.05, 0.4, 0.8,1))
plt.legend(ncol=2, fontsize=8)
plt.xlabel('Rate (rps)', font)
plt.ylabel('P99 Delay (s)', font)
plt.subplots_adjust(left = 0.15, right=0.97, bottom=0.31, top=0.95)


# print(RATES[0:len(results["WRR"])], results["WRR"])
if save_or_show == 0:
	plt.savefig("p4hauler_vs_cheetah.pdf")
	plt.show()
else:
	plt.savefig("p4hauler_vs_cheetah.pdf")
	plt.show()
