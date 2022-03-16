import sys
import re
import pandas as pd
import numpy as np

def snap(in_str):
	if True:
		out_str = ""
		li = list( re.compile('[a-zA-Z0-9]+').finditer(in_str) )
		if len(li) < 4:
			return None
		l = list( re.compile('[a-zA-Z0-9]+').finditer(in_str) )[-4].start()
		li = list( re.compile('[a-zA-Z0-9]+').finditer(in_str) )
		if len(li) < 4:
			return None
		r = list( re.compile('[a-zA-Z0-9]+').finditer(in_str) )[-4].end()
		out_str += in_str[l:r]
		return out_str

def getIO(path):
	data = pd.read_csv(path, dtype=str, header=None, quotechar="'")
	ins = np.array(data[0]).tolist()
	if len(list(data.columns)) < 2:
		outs = [float('NaN')] * len(ins)
	else:
		outs = np.array(data[1]).tolist()
	return ins, outs

if len(sys.argv) < 2 or '.csv' not in sys.argv[1]:
	print('Useage: python3 snap.py [filename].csv')
	print('Assumes: each line has at most 2 columns, optionally quoted by \'s')
	print('Output: file called snap-[filename].csv where each empty output column is filled')
	sys.exit()
ins, outs = getIO(sys.argv[1])
for i in range(len(outs)):
	if outs[i] != outs[i]:
		outs[i] = snap(ins[i])
		outs[i] = '---SynthError---' if not outs[i] else outs[i]

li = re.split('[/\\\\]', sys.argv[1])
li = [x for x in li if x]
li[-1] = 'snap-' + li[-1]
sep = '\\' if '\\' in sys.argv[1] else '/'
name = sep.join(li)
file = open(name, mode='w')
for i in range(len(outs)):
	file.write('\'' + ins[i]  + '\',')
	file.write('\'' + outs[i] + '\'\n')
file.close()