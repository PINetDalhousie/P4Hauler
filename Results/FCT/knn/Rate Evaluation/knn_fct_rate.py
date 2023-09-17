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

RATES	= range(8,21,2)

RESULTS_TYPE = "FCT:"

def read_data(r_type):
	results = {}
	for p in list_of_policies: results[p] = []

	for d in list_of_policies:
		for r in RATES:
			file = open("./" + d + "/" + str(r) + ".log", "r")
			s = 0
			for line in file:
				l = line.strip().split()
				if len(l)> 0 and l[0] == r_type:
					s += float(l[-1])
			results[d].append(s/10)
			file.close()
	return results


results = read_data(RESULTS_TYPE)
# for r in results:
# 	print(r,results[r])

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
plt.plot(RATES[0:len(results["LSU"])], results["LSU"], marker='s' ,label= "LUR", linestyle="solid", color = "purple", mfc="none")  # Plot the chart
plt.plot(RATES[0:len(results["PRT"])], results["PRT"], marker='^' ,label= "PRT", linestyle="solid", color = "green", mfc="none")  # Plot the chart
plt.plot(RATES[0:len(results["WRR"])], results["WRR"], marker='x' ,label= "WRR", linestyle="solid", color = "red", mfc="none")  # Plot the chart
# plt.yscale("log")
plt.xlim(8,20)
plt.ylim(10,35)


plt.tick_params(axis='both', which='major', labelsize=12)
plt.xticks(np.arange(8, 21, step=4))
plt.yticks(np.arange(10, 41, step=10))


# plt.legend(ncol=2, fontsize=8, bbox_to_anchor=(-0.1, 0.41, 1,1))
plt.legend(fontsize=12)

plt.xlabel('Rate (rps)', font)
plt.ylabel('Time (s)', font)
# plt.subplots_adjust(left = 0.18, right=0.97, bottom=0.22, top=0.79)
plt.subplots_adjust(left = 0.17, right=0.97, bottom=0.16, top=0.97)

for i,j in zip(results["Server-Only"], RATES[0:len(results["Server-Only"])]):
	print(i, j ,100/i)
print("*******************")

for i,j in zip(results["WRR"], RATES[0:len(results["Server-Only"])]):
	print(i, j ,100/i)
# print(results["Server-Only"])
# print()

if save_or_show == 0:
	# plt.show()
	plt.savefig("../../knn_FCT_rate_evaluation.pdf")
else:
	plt.show()
	# plt.savefig("vgg_thr.pdf", bbox_inches='tight')
	plt.savefig("../../knn_FCT_rate_evaluation.pdf")
# 