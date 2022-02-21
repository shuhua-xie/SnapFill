import Synthesizer as Synth
import sys
import pandas as pd
import numpy as np

# this methods takes in a path to a csv file with the format input,output\n 
# and separates the inputs and outputs
#
# how to use:
# input, output = getInputOutput(path to csv)
def getInputOutput(path):
    data = pd.read_csv(path, dtype=str, header=None)
    return np.array(data[0]).tolist(),np.array(data[1]).tolist()

def getBenchmarkConstraints(path):
    file = open(path)

    text = file.readlines()
    constraints = []

    for i in range(len(text)):
        if "constraint" in text[i]:
            constraints.append(text[i][18:-3].split(")"))

    inputs = []
    outputs = []

    for i in range(len(constraints)):
        inputs.append(constraints[i][0].split("\"")[1])
        outputs.append(constraints[i][1].split("\"")[1])

    return inputs,outputs
        

# For demo purposes only!
if len(sys.argv) != 2:
    print("Usage: python SnapFill.py input_file.[sl/csv]")
    sys.exit()

if ".csv" in sys.argv[1]:
    in_arr, out_arr = getInputOutput(sys.argv[1])
elif ".sl" in sys.argv[1]:
    in_arr, out_arr = getBenchmarkConstraints(sys.argv[1])

print("--debug info-- inputs: " + str(in_arr))
print("--debug info-- outputs: " + str(out_arr))
print()

snap_fill = Synth.Synthesizer(in_arr, out_arr)

for k in snap_fill.synth_DAG.edges.keys():
    print("Programs represented by edge (" + str(k[0]) + " -->\n" + str(k[1]) + "):")
    substr_set = snap_fill.synth_DAG.edges[k]
    for s in substr_set:
        s.print_progs(snap_fill.synth_IDG)
if (not snap_fill.synth_DAG.edges.keys()):
    print("No program could be synthesized")
sys.exit()
