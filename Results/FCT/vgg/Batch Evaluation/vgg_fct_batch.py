import matplotlib.pyplot as plt
import numpy as np
import argparse
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 

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


RATES	= range(400,1001,100)

RESULTS_TYPE = "FCT:"

def read_data(r_type):
	results = {}
	for p in list_of_policies: results[p] = []

	for d in list_of_policies:
		for r in RATES:
			file = open("./" + d + "/60-" + str(r) + ".log", "r")
			s = 0
			for line in file:
				l = line.strip().split()
				if len(l)> 0 and l[0] == r_type:
					s += float(l[-1])
			results[d].append(s/10)
			file.close()
	return results


results = read_data(RESULTS_TYPE)

print(results)
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
# plt.yscale("log")
plt.xlim(400,1000)
plt.ylim(5,20)


plt.tick_params(axis='both', which='major', labelsize=11)
plt.xticks(np.arange(400, 1001, step=200))
plt.yticks(np.arange(5, 25, 5))


# plt.legend(ncol=2, fontsize=8, bbox_to_anchor=(-0.1, 0.41, 1,1))
# plt.legend(fontsize=10, loc="upper left")

plt.xlabel('Total Number of Requests', font)
plt.ylabel('Time (s)', font)

plt.legend(ncol=2, fontsize=12, bbox_to_anchor=(0.05, 0.404, 1,1))
# plt.legend(ncol=2, fontsize=12, loc="upper left")

plt.subplots_adjust(left = 0.17, right=0.94, bottom=0.16, top=0.77)
# plt.subplots_adjust(left = 0.14, right=0.95, bottom=0.17, top=0.96)

# axins =ax.inset_axes([0.5, 0.5, 0.47, 0.47])
# ax.indicate_inset_zoom(axins, edgecolor="black")


if save_or_show == 0:
	# plt.show()
	plt.savefig("../../vgg_FCT_batch_evaluation_60.pdf")
else:
	# plt.savefig("vgg_thr.pdf", bbox_inches='tight')
	plt.savefig("vgg_FCT_batch_evaluation_70.pdf")
