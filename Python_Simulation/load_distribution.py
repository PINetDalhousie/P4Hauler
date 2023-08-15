from simulation import *
import matplotlib.pyplot as plt
import numpy as np


SERVER = 64
ACCElERATOR = 2

ITERATION = 100
# LOAD = SERVER * 20

print('baseline:')
rate = 64*20


util = {"base":np.zeros(64), "lsu":np.zeros(64*(ACCElERATOR+1)), "prt":np.zeros(64*(ACCElERATOR+1)), "wrr":np.zeros(64*(ACCElERATOR+1))}


for i in range(ITERATION):
	load_base_64, util_base_64, lat_base_64 =  baseline(rate, SERVER, ACCElERATOR)
	util["base"] += util_base_64[::3]

	load_lsu_64, util_lsu_64, lat_lsu_64 = lsu(rate, SERVER, ACCElERATOR)
	# print(util_lsu_64)
	util["lsu"] += util_lsu_64

	load_prt_64, util_prt_64, lat_prt_64 = priority(rate, SERVER, ACCElERATOR)
	util["prt"] += util_prt_64

	load_wrr_64, util_wrr_64, lat_wrr_64 = wrr3(rate, SERVER, ACCElERATOR)
	util["wrr"] += util_wrr_64

util["base"] /= ITERATION
util["lsu"] /= ITERATION
util["prt"] /= ITERATION
util["wrr"] /= ITERATION

plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 13,
}

fig, ax1 = plt.subplots(figsize=(5.5,3))
ax1.set_ylabel("Variances across device utilization (%)", font)
ax1.set_xlabel("Servers", font)
ax1.set_ylim(0, 200)



bp1 = ax1.boxplot(util["base"],positions=[1], sym='', patch_artist=True, boxprops=dict(facecolor="blue"), medianprops=dict(color="blue"))
bp2 = ax1.boxplot(util["lsu"], positions=[2], sym='', patch_artist=True, boxprops=dict(facecolor="purple"), medianprops=dict(color="purple"))
bp3 = ax1.boxplot(util["prt"], positions=[3], sym='', patch_artist=True, boxprops=dict(facecolor="green"), medianprops=dict(color="green"))
bp4 = ax1.boxplot(util["wrr"], positions=[4], sym='', patch_artist=True, boxprops=dict(facecolor="red"), medianprops=dict(color="red"))

# print(util)

ax1.legend([bp1["boxes"][0], bp2["boxes"][0], bp3["boxes"][0], bp4["boxes"][0]], ['Server-Only', 'LSU', "PRT", "WRR"], loc='upper right')


labels = ["Server-Only", "LSU", "PRT", "WRR"]
plt.xticks(np.arange(1,5, 1), labels, fontsize=11)
plt.subplots_adjust(left = 0.11, right=0.97, bottom=0.16, top=0.82)
# plt.savefig("load_dist.pdf")

plt.show()

