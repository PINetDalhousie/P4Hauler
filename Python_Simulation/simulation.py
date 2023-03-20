import random
import numpy as np



_server_cap = 16
_accele_cap = 4

_server_threshhold = 90
_accele_threshhold = 95

_server_lat = 300
_accele_lat = 1000


def calc_throughput(load, util):
	i, length = 0, len(util)
	throughput = 0
	while (i < length):
		if util[i] <= 100:
			throughput+=load[i]
		elif util[i] < 105: 
			# throughput += load[i]*util[i]/100
			throughput += load[i]*0.5
		i+=1
	return throughput





def baseline(_rate, _servers, _accelerators):
	_load = np.zeros(_servers*(_accelerators+1))
	_util = np.zeros(_servers*(_accelerators+1))
	_lats = np.zeros(_servers*(_accelerators+1))

	for r in range(_rate):
		selected_s = np.random.randint(0, _servers)
		_load[selected_s*(_accelerators+1)] += 1
		_util[selected_s*(_accelerators+1)] += np.random.normal(100/_server_cap, 1)

	for i in range(0,len(_lats), _accelerators+1):
		if _util[i] < _server_threshhold:
			_lats[i] = np.random.normal(_server_lat,0.1*_server_lat)
		else:
			_lats[i] = _load[i] * np.random.normal(350, 35) - np.random.normal(3500, 350)

	return _load, _util, _lats


def lsu(_rate, _servers, _accelerators):
	_load = np.zeros(_servers*(_accelerators+1))
	_util = np.zeros(_servers*(_accelerators+1))
	_lats = np.zeros(_servers*(_accelerators+1))
	# print(_rate)
	for r in range(_rate):
		selected_s = np.random.randint(0, _servers)
		u_ = _util[selected_s*(_accelerators+1): selected_s*(_accelerators+1) + _accelerators +1]
		index_min = np.argmin(u_)
		if index_min == 0:
			_load[selected_s*(_accelerators+1)] += 1
			_util[selected_s*(_accelerators+1)] += np.random.normal(100/_server_cap, 1)

		else:
			_load[selected_s*(_accelerators+1)+index_min] += 1
			_util[selected_s*(_accelerators+1)+index_min] += (np.random.normal(100/_accele_cap, 1) + 0.1*np.random.normal(_util[selected_s*(_accelerators+1)+index_min], 1))
			# _util[selected_s*(_accelerators+1)+index_min] += (np.random.normal(100/_accele_cap, 1))


	for i in range(len(_lats)):
		if i%(_accelerators+1)==0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_server_lat,0.1*_server_lat)
			else:
				_lats[i] = _load[i] * np.random.normal(350, 35) - np.random.normal(3500, 350)
		elif _util[i] != 0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_accele_lat,0.1*_accele_lat)
			else:
				_lats[i] =  _load[i] * np.random.normal(400, 40) + np.random.normal(1200, 120)

	return _load, _util, _lats


def priority(_rate, _servers, _accelerators):
	_load = np.zeros(_servers*(_accelerators+1))
	_util = np.zeros(_servers*(_accelerators+1))
	_lats = np.zeros(_servers*(_accelerators+1))

	for r in range(_rate):
		selected_s = np.random.randint(0, _servers)
		if _util[selected_s*(_accelerators+1)] <= _server_threshhold:
			_load[selected_s*(_accelerators+1)] += 1
			_util[selected_s*(_accelerators+1)] += np.random.normal(100/_server_cap, 1)

		else:
			u_ = _util[selected_s*(_accelerators+1): selected_s*(_accelerators+1) + _accelerators +1]
			index_min = np.argmin(u_)
			_load[selected_s*(_accelerators+1)+index_min] += 1
			_util[selected_s*(_accelerators+1)+index_min] += np.random.normal(100/_accele_cap, 1)


	for i in range(len(_lats)):
		if i%(_accelerators+1)==0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_server_lat,0.1*_server_lat)
			else:
				_lats[i] = _load[i] * np.random.normal(350, 35) - np.random.normal(3500, 350)
		elif _util[i] != 0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_accele_lat,0.1*_accele_lat)
			else:
				_lats[i] =  _load[i] * np.random.normal(250, 25) + np.random.normal(1000, 100)

	return _load, _util, _lats

def wrr(_rate, _servers, _accelerators):
	_load = np.zeros(_servers*(_accelerators+1))
	_util = np.zeros(_servers*(_accelerators+1))
	_lats = np.zeros(_servers*(_accelerators+1))
	# print(_rate)
	for r in range(_rate):
		selected_s = np.random.randint(0, _servers)
		# u_ = _util[selected_s*(_accelerators+1): selected_s*(_accelerators+1) + _accelerators +1]
		selected_d = np.random.randint(0,_server_cap + _accelerators*_accele_cap)
		index_min = 0
		if selected_d >= _server_cap:
			selected_d -= _server_cap
			index_min = int(selected_d/_accele_cap) +1

		# index_min = np.argmin(u_)
		if index_min == 0:
			_load[selected_s*(_accelerators+1)] += 1
			_util[selected_s*(_accelerators+1)] += np.random.normal(100/_server_cap, 0.2)

		else:
			_load[selected_s*(_accelerators+1)+index_min] += 1
			_util[selected_s*(_accelerators+1)+index_min] += np.random.normal(100/_accele_cap, 1)


	for i in range(len(_lats)):
		if i%(_accelerators+1)==0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_server_lat,0.1*_server_lat)
			else:
				_lats[i] = _load[i] * np.random.normal(350, 35) - np.random.normal(3500, 350)
		elif _util[i] != 0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_accele_lat,0.1*_accele_lat)
			else:
				_lats[i] =  _load[i] * np.random.normal(250, 25) + np.random.normal(1000, 100)

	return _load, _util, _lats


def wrr2(_rate, _servers, _accelerators):
	_load = np.zeros(_servers*(_accelerators+1))
	_util = np.zeros(_servers*(_accelerators+1))
	_lats = np.zeros(_servers*(_accelerators+1))
	# print(_rate)
	for r in range(_rate):
		selected_s = np.argmin(_util[::_accelerators+1])

		u_ = _util[selected_s*(_accelerators+1): selected_s*(_accelerators+1) + _accelerators +1]
		index_min = np.argmin(u_)

		if index_min == 0:
			_load[selected_s*(_accelerators+1)] += 1
			_util[selected_s*(_accelerators+1)] += np.random.normal(100/_server_cap, 0.2)

		else:
			_load[selected_s*(_accelerators+1)+index_min] += 1
			_util[selected_s*(_accelerators+1)+index_min] += np.random.normal(100/_accele_cap, 0.2)


	for i in range(len(_lats)):
		if i%(_accelerators+1)==0:
			if _util[i] <= 100:
				_lats[i] = np.random.normal(_server_lat,0.1*_server_lat)
			else:
				_lats[i] = _load[i] * np.random.normal(350, 35) - np.random.normal(3500, 350)
		elif _util[i] != 0:
			if _util[i] <= 100:
				_lats[i] = np.random.normal(_accele_lat,0.1*_accele_lat)
			else:
				_lats[i] =  _load[i] * np.random.normal(250, 25) + np.random.normal(1000, 100)

	return _load, _util, _lats




def wrr3(_rate, _servers, _accelerators):
	_load = np.zeros(_servers*(_accelerators+1))
	_util = np.zeros(_servers*(_accelerators+1))
	_lats = np.zeros(_servers*(_accelerators+1))


	rate_per_server = int(_rate/_servers)
	rate_server_list = [rate_per_server]*_servers
	index = 0
	while sum(rate_server_list) < _rate:
		rate_server_list[index] += 1
		index += 1
	# print(rate_server_list)

	for i in range(len(rate_server_list)):
		total_rate = rate_server_list[i]
		rate_server = int(np.ceil((total_rate * (_server_cap/(_server_cap + _accelerators*_accele_cap)))))
		rate_accelerator = total_rate - rate_server
		_load[i*(_accelerators+1)] = rate_server
		_util[i*(_accelerators+1)] = rate_server * np.random.normal(100/_server_cap, 2)
		rate_accelerator_list = [int(rate_accelerator/_accelerators)] * _accelerators
		index = 0
		while sum(rate_accelerator_list) < rate_accelerator:
			rate_accelerator_list[index] += 1
			index += 1
		for ac in range(1,_accelerators+1):
			_load[i*(_accelerators+1)+ac] = rate_accelerator_list[ac-1]
			_util[i*(_accelerators+1)+ac] = rate_accelerator_list[ac-1] *np.random.normal(100/_accele_cap, 2)


	for i in range(len(_lats)):
		if i%(_accelerators+1)==0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_server_lat,0.1*_server_lat)
			else:
				_lats[i] = _load[i] * np.random.normal(350, 35) - np.random.normal(3500, 350)
		elif _util[i] != 0:
			if _util[i] < 100:
				_lats[i] = np.random.normal(_accele_lat,0.1*_accele_lat)
			else:
				_lats[i] =  _load[i] * np.random.normal(250, 25) + np.random.normal(1000, 100)

	return _load, _util, _lats

