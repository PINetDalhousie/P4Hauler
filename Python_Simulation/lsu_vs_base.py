import random
import numpy as np
import matplotlib.pyplot as plt


_servers = 64
_accelerator = 2

_server_cap = 16
_accele_cap = 4


# _rate = _servers * _server_cap + _servers*2*_accele_cap
_rate = 4500

_load = np.zeros(_servers*(_accelerator+1))
_util = np.zeros(_servers*(_accelerator+1))


def baseline(_rate = 1200, _servers=64, _accelerator=2):
	_load = np.zeros(_servers*(_accelerator+1))
	_util = np.zeros(_servers*(_accelerator+1))
	for r in range(_rate):
		selected_s = random.randint(0, _servers-1)
		_load[selected_s*3] += 1
		_util[selected_s*3] += 2
	return _load, _util


def lsu(_rate = 1200, _servers=64, _accelerator=2):
	_load = np.zeros(_servers*(_accelerator+1))
	_util = np.zeros(_servers*(_accelerator+1))
	for r in range(_rate):
		selected_s = random.randint(0, _servers-1)
		if _util[selected_s*3] <= _util[selected_s*3+1] and _util[selected_s*3] <= _util[selected_s*3+2]:
			_load[selected_s*3] += 1
			_util[selected_s*3] += 2

		elif _util[selected_s*3+1] < _util[selected_s*3] and _util[selected_s*3+1] <= _util[selected_s*3+2]:
			_load[selected_s*3+1] += 1
			_util[selected_s*3+1] += 10	

		elif _util[selected_s*3+2] < _util[selected_s*3] and _util[selected_s*3+2] < _util[selected_s*3+1]:
			_load[selected_s*3+2] += 1
			_util[selected_s*3+2] += 10	

	return _load, _util


def count_fail(_load):
	fails = 0
	for i in range(len(_load)):
		if i%3==0 and _load[i]>55:
			fails+=1
		elif i%3!=0 and _load[i]>12:
			fails+=1

	return fails, fails/len(_load)

def main():
	_load, _util = baseline()
	# _load, _util = lsu()

	print(count_fail(_load))

	#Plotting
	plt.rcParams.update({
	    'font.family': 'Times New Roman',
	    # "font.weight": "bold",
	    # "axes.labelweight": "bold"
	})

	font = {'family' : 'Times New Roman',
	# 'weight' : 'bold',
	'size' : 16,
	}


	fig, ax1 = plt.subplots(figsize=(7,2))
	x = np.arange(len(_load))
	ax1.set_ylabel("Obtained Rate (rps)", font)
	ax1.set_xlabel("Devices ID", font)
	ax1.xaxis.set_label_coords(.5, -0.1)
	ax1.yaxis.set_label_coords(-0.07, 0.41)
	ax1.set_ylim(0, 32)
	ax1.set_xlim(0, len(_load))

	ax1.scatter(x[::3], _load[::3],label= "Hosts' loads", color = "g", marker = "x")

	ax1.scatter(x[1::3], _load[1::3],label= "Accelerators' loads", color = "tab:green", marker = ".")
	ax1.scatter(x[2::3], _load[2::3], color = "tab:green", marker = ".")

	ax1.axhline(y = 16, color = 'tab:red', linestyle = 'dotted')
	ax1.axhline(y = 4, color = 'red', linestyle = 'dashed')
	# ax1.axhline(y = 55, color = 'tab:red')
	# ax1.axhline(y = 12, color = 'tab:red')

	ax1.legend(fontsize=12, loc="upper left")
	plt.tick_params(axis='both', which='major', labelsize=14)
	# _load = _load**-1
	# ax2 = ax1.twinx()
	# ax2.set_ylabel("Overhead on CPU (%)", font)
	# # ax2.set_ylim(0,15)
	# ax2.plot(x, _load, marker='o' ,label= "99th Latency(s)", linestyle="--", color = "c")  # Plot the chart
	# ax2.legend(fontsize=8, loc="upper right")

	plt.xticks(np.arange(0, len(_load)+1, step=64))
	plt.subplots_adjust(left = 0.095, right=0.98, bottom=0.17, top=0.98)

	plt.savefig("baseline.pdf")
	plt.show()

# Using the special variable 
# __name__
if __name__=="__main__":
    main()