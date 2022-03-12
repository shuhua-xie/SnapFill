import pandas as pd
import numpy as np
import sys


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

def main():
    ins, outs = getBenchmarkConstraints(sys.argv[1])
    name = sys.argv[1].split(".")[0] + ".csv"
    file = open(name, 'w')
    for i in range(len(ins)):
        line = "'" + ins[i] + "',"
        if outs[i] == outs[i]:
            line += "'" + outs[i] + "'"
        line += "\n"
        file.write(line)
    return

if __name__ == "__main__":
    main()
