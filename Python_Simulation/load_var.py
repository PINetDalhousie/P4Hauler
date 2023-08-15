from simulation import *
import matplotlib.pyplot as plt
import numpy as np
import pickle 


# SERVER = 64
# ACCElERATOR = 2

# ITERATION = 10000

# rate = 1300


# util = {"base":[], "lsu":[], "prt":[], "wrr":[]}


# for i in range(ITERATION):
# 	# if i%100 == 0:
# 	# 	print(i)
# 	load_base_64, util_base_64, lat_base_64 =  baseline(rate, SERVER, ACCElERATOR)
# 	# util["base"].append(np.var(util_base_64)/100)
# 	util["base"].append(np.var(util_base_64[::3])/100)
# 	# print(np.var(util_base_64[::3]))

# 	load_lsu_64, util_lsu_64, lat_lsu_64 = lsu(rate, SERVER, ACCElERATOR)
# 	# util["lsu"] += util_lsu_64
# 	util["lsu"].append(np.var(util_lsu_64)/100)

# 	load_prt_64, util_prt_64, lat_prt_64 = priority(rate, SERVER, ACCElERATOR)
# 	# util["prt"] += util_prt_64
# 	util["prt"].append(np.var(util_prt_64)/100)
# 	# print(util_prt_64)

# 	load_wrr_64, util_wrr_64, lat_wrr_64 = wrr3(rate, SERVER, ACCElERATOR)
# 	# util["wrr"] += util_wrr_64
# 	util["wrr"].append(np.var(util_wrr_64)/100)


# SERVER = 128
# ACCElERATOR = 2


# rate = 2600
# util_128 = {"base":[], "lsu":[], "prt":[], "wrr":[]}

# for i in range(ITERATION):

# 	load_base_64, util_base_64, lat_base_64 =  baseline(rate, SERVER, ACCElERATOR)
# 	util_128["base"].append(np.var(util_base_64[::3])/100)

# 	load_lsu_64, util_lsu_64, lat_lsu_64 = lsu(rate, SERVER, ACCElERATOR)
# 	util_128["lsu"].append(np.var(util_lsu_64)/100)

# 	load_prt_64, util_prt_64, lat_prt_64 = priority(rate, SERVER, ACCElERATOR)
# 	util_128["prt"].append(np.var(util_prt_64)/100)

# 	load_wrr_64, util_wrr_64, lat_wrr_64 = wrr3(rate, SERVER, ACCElERATOR)
# 	util_128["wrr"].append(np.var(util_wrr_64)/100)



# with open('64.pkl', 'wb') as f:
#     pickle.dump(util, f)


# with open('128.pkl', 'wb') as f:
#     pickle.dump(util_128, f)



with open('64.pkl', 'rb') as f:
    util = pickle.load(f)

with open('128.pkl', 'rb') as f:
    util_128 = pickle.load(f)


plt.rcParams.update({
    'font.family': 'Times New Roman',
    # "font.weight": "bold",
    # "axes.labelweight": "bold"
})

font = {'family' : 'Times New Roman',
# 'weight' : 'bold',
'size' : 10,
}

fig, ax1 = plt.subplots(figsize=(3,2))
ax1.set_ylabel("Variances across device\nutilization (%)", font)
# ax1.set_xlabel("Servers", font)
# ax1.set_ylim(0, 200)



bp1 = ax1.boxplot(util["base"],positions=[0.1], sym='', patch_artist=True, boxprops=dict(facecolor="tab:blue"), medianprops=dict(linewidth=0), widths = 0.05)
bp2 = ax1.boxplot(util["lsu"], positions=[0.2], sym='', patch_artist=True, boxprops=dict(facecolor="tab:purple"), medianprops=dict(linewidth=0), widths = 0.05)
bp3 = ax1.boxplot(util["prt"], positions=[0.3], sym='', patch_artist=True, boxprops=dict(facecolor="tab:green"), medianprops=dict(linewidth=0), widths = 0.05)
bp4 = ax1.boxplot(util["wrr"], positions=[0.4], sym='', patch_artist=True, boxprops=dict(facecolor="tab:red"), medianprops=dict(linewidth=0), widths = 0.05)



bp5 = ax1.boxplot(util_128["base"],positions=[0.6], sym='', patch_artist=True, boxprops=dict(facecolor="tab:blue"), medianprops=dict(linewidth=0), widths = 0.05)
bp6 = ax1.boxplot(util_128["lsu"], positions=[0.7], sym='', patch_artist=True, boxprops=dict(facecolor="tab:purple"), medianprops=dict(linewidth=0), widths = 0.05)
bp7 = ax1.boxplot(util_128["prt"], positions=[0.8], sym='', patch_artist=True, boxprops=dict(facecolor="tab:green"), medianprops=dict(linewidth=0), widths = 0.05)
bp8 = ax1.boxplot(util_128["wrr"], positions=[0.9], sym='', patch_artist=True, boxprops=dict(facecolor="tab:red"), medianprops=dict(linewidth=0), widths = 0.05)

ax1.set_xlim(0,1)
ax1.set_ylim(2, 25)
# print(util)

ax1.legend([bp1["boxes"][0], bp2["boxes"][0], bp3["boxes"][0], bp4["boxes"][0]], ['Server-Only', 'LSU', "PRT", "WRR"],
	bbox_to_anchor=(0.04, 0.18, 0.97,1),
	ncol=4,
	fontsize=7)

labels = ["64 Servers", "128 Servers"]
plt.xticks(np.arange(0.25, 1, 0.5), labels, fontsize=10)

labels = ["5", "15", "25"]
plt.yticks(np.arange(5, 26, 10), labels, fontsize=10)

plt.subplots_adjust(left = 0.2, right=0.98, bottom=0.11, top=0.88)


plt.savefig("load_var.pdf")
 
plt.show()

