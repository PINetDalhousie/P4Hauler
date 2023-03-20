import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
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
RATES	= range(2,21,2)

def read_cpu():
	results_1 = {}
	results_2 = {}
	for p in list_of_policies:
		results_1[p] = []
		results_2[p] = []

	for d in list_of_policies:
		file = open("./" + d + "/CPU.log", "r")
		for line in file:
			l = line.strip().split()
			if l[4] == "CPU":
				try:
					results_1[d].append(float(l[6]))
					results_2[d].append(float(l[7]))
				except:
					pass
		file.close()
	return results_1, results_2




results_server, results_smartnic = read_cpu()
for p in results_server:
	print(results_server[p], results_smartnic[p])


# width = 1
# RATES = np.array(RATES)
# plt.figure(figsize=(6,3))

# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["axes.labelweight"] = "bold"

# plt.bar(RATES[0:len(results_server["Server-Only"])] - 2*width , results_server["Server-Only"], width= width,label='Server-Only', color = "tab:blue", hatch="|||")

# plt.bar(RATES[0:len(results_server["WRR"])] - 1*width , results_server["WRR"], width= width,label='WRR-SERVER', color = "tab:red", hatch = '+++')
# plt.bar(RATES[0:len(results_smartnic["WRR"])] - 1*width, results_smartnic["WRR"], width= width,label='WRR-SMARTNIC', bottom=results_server["WRR"],color = "tab:orange", hatch = "xxx")

# plt.bar(RATES[0:len(results_server["WRR"])] , results_server["PRT"], width= width,label='PRT-SERVER', color = "tab:purple", hatch = "ooo")
# plt.bar(RATES[0:len(results_smartnic["WRR"])] , results_smartnic["PRT"], width= width,label='PRT-SMARTNIC',bottom=results_server["PRT"], color = "tab:cyan", hatch = "...")

# plt.bar(RATES[0:len(results_server["LSU"])] + width , results_server["LSU"], width= width,label='LSU-SERVER', color = "tab:green", hatch = "///")
# plt.bar(RATES[0:len(results_smartnic["LSU"])] + width, results_smartnic["LSU"], width= width,label='LSU-SMARTNIC',bottom=results_server["LSU"],color = "tab:olive", hatch = "\\\\\\")


# plt.tick_params(axis='both', which='major', labelsize=12)
# plt.xticks(np.arange(10, 71, step=20))


# plt.xlabel('Rate (rps)', fontweight='bold', fontsize=14)
# plt.ylabel('CPU Utilization (%)', fontweight='bold', fontsize=14)

# plt.xlim(7,72)
# plt.subplots_adjust(left = 0.13, right=0.98, bottom=0.17, top=0.95)
# plt.legend(ncol=2, fontsize=8)

######################################################################################################

figure, axis = plt.subplots(1,4 , figsize=(11,2))

plt.rcParams.update({
    'font.family': 'Times New Roman',
    "font.weight": "bold",
    "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
'weight' : 'bold',
'size' : 12,
}

fm = FontProperties(weight='bold')

width=2/3
RATES = np.array(RATES)
axis[0].bar(RATES[0:len(results_server["Server-Only"])] - width/2, results_server["Server-Only"], width= width,label="Server's CPU", color = "tab:blue", hatch="ooo")
axis[0].bar(RATES[0:len(results_smartnic["Server-Only"])] + width/2, results_smartnic["Server-Only"], width= width,label="SmartNIC's CPU",color = "tab:red", hatch = "xxx")
axis[0].set_title("Only Server or SmartNIC",font)



axis[1].bar(RATES[0:len(results_server["WRR"])] - width/2 , results_server["WRR"], width= width,label="Server's CPU", color = "tab:blue", hatch = 'ooo')
axis[1].bar(RATES[0:len(results_smartnic["WRR"])] + width/2, results_smartnic["WRR"], width= width,label="SmartNIC's CPU",color = "tab:red", hatch = "xxx")
axis[1].set_title("WRR", font)


axis[2].bar(RATES[0:len(results_server["PRT"])] - width/2 , results_server["PRT"], width= width,label="Server's CPU", color = "tab:blue", hatch = 'ooo')
axis[2].bar(RATES[0:len(results_smartnic["PRT"])] + width/2, results_smartnic["PRT"], width= width,label="SmartNIC's CPU",color = "tab:red", hatch = "xxx")
axis[2].set_title("PRT", font)




axis[3].bar(RATES[0:len(results_server["LSU"])] - width/2 , results_server["LSU"], width= width,label="Server's CPU", color = "tab:blue", hatch = 'ooo')
axis[3].bar(RATES[0:len(results_smartnic["LSU"])] + width/2, results_smartnic["LSU"], width= width,label="SmartNIC's CPU",color = "tab:red", hatch = "xxx")
axis[3].set_title("LSU", font)


for ax in axis:
	ax.set_xticks(np.arange(2, 21, step=2))
	ax.set_yticks(np.arange(0, 101, step=50))
	ax.set_xticklabels(ax.get_xticks(), weight='bold', size=8, font="Times New Roman")
	ax.set_yticklabels(ax.get_yticks(), weight='bold', size=8, font="Times New Roman")
	ax.set_ylabel('CPU Utilization (%)', font)
	ax.set_xlabel("Rate (RPS)", font)
	ax.axis(xmin=1,xmax=21)

	# axis[1].get_yaxis().set_visible(False)
axis[1].legend(ncol=1,fontsize=8)
plt.subplots_adjust(wspace=0.28, hspace=0)
plt.subplots_adjust(left = 0.05, right=0.997, bottom=0.21, top=0.89)

if save_or_show == 0:
	plt.show()
else:
	plt.savefig("knn_cpu.pdf")
	# plt.savefig("vgg_cpu.pdf", bbox_inches='tight')

