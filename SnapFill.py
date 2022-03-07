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
    data = pd.read_csv(path, dtype=str, header=None, quotechar="'")
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

if (not snap_fill.pairs):
    print("No program could be synthesized")
    sys.exit()

for i in range(len(snap_fill.pairs)):
    print("Branch " + str(i) + "----------")
    # print(snap_fill.pairs[i][1])
    print("Nodes:")
    for n in snap_fill.pairs[i][1].nodes:
        print(n)
#    print("Edges:")
#    for e in snap_fill.pairs[i][1].edges.keys():
#        print(e[0].__str__() + " to " + e[1].__str__())
    print("Branch " + str(i) + " end------\n")
