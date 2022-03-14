import Synthesizer as Synth
import sys
import getopt
import pandas as pd
import numpy as np

# this methods takes in a path to a csv file with the format input,output\n 
# and separates the inputs and outputs
#
# how to use:
# input, output = getInputOutput(path to csv)
def getInputOutput(path):
    data = pd.read_csv(path, dtype=str, header=None, quotechar="'")
    ins = np.array(data[0]).tolist()
    if len(list(data.columns)) < 2:
        outs = [float('NaN')] * len(ins)
    else:
        outs = np.array(data[1]).tolist()
    return ins, outs

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

def shell_help():
    print("---SnapFill Shell---")
    print("commands available:")
    print("help: displays this message")
    print("exit: exit shell")
    print("print: print the current program in SnapFill DSL")
    print("list [branch | substring | cond | start_pat | end_pat]: lists the options available for each")
    print("\t(note that branch must be set to list substring and substring must be set to list patterns)")
    print("set [branch | substring] n: set the branch or substring to work on, n must be a nonnegative integer")
    print("change [cond | start_pat | end_pat] n: change the branching condition or regex pattern")
    print("where: print set branch and substring")
    print("output <optional name with no spaces>: output current program in python to the specified file or snap.py by default")
    print()

def main():
    help_str  = "Usage: python3 SnapFill.py [input_file].csv [options]\n"
    help_str += "options: -dfghops\n"
    help_str += "\t-d: print synthesized program in FlashFill DSL (a variant of it)\n\t\tdefault if no options specified\n"
    help_str += "\t-f: synthesize as FlashFill did (without branches)\n"
    help_str += "\t-g: print debug info (inputs and outputs passed to the program)\n"
    help_str += "\t-h: prints this help message\n"
    help_str += "\t-o <output_file>: print python program into output_file\n"
    help_str += "\t-p: print synthesized program in python\n"
    help_str += "\t-s: shell mode (Not very tested)\n"
    
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "dfgho:ps")
    except getopt.GetoptError as err:
        print(err)
        print(help_str)
        sys.exit(1)
    
    if len(args) != 1 or ".csv" not in args[0]:
        print("Error: exactly 1 input file expected (in csv form)")
        print(args)
        print(opts)
        print(help_str)
        sys.exit(1)
    
    opts = dict(opts)
    if ("-h" in opts):
        print(help_str)
        sys.exit(1)
    
    debug = "-g" in opts
    in_arr, out_arr = getInputOutput(args[0])
    if (debug):
        print("--debug info-- inputs: " + str(in_arr))
        print("--debug info-- outputs: " + str(out_arr))
        print()
    
    snap_fill = Synth.Synthesizer(in_arr, out_arr, "-f" in opts)
    if  snap_fill.error:
        print(snap_fill.error)
        print("No program could be synthesized")
        sys.exit()
    
    bp = snap_fill.best_prog
    if ("-d" in opts or not opts or (len(opts) == 1 and "-f" in opts)):
        print(bp)
    if ("-p" in opts):
        print(bp.to_python())
    if ("-o" in opts):
        fname = opts["-o"] 
        f = open(fname, 'w')
        f.write(bp.to_python())
        f.close()
    if ("-s" in opts and not "-f" in opts):
        print("Work In Progress")
        print("Welcome to SnapFill shell!")
        branch = None
        conds = None
        substr = None
        starts = None
        ends = None
        while True:
            raw = input(">>> ")
            line = raw.split()
            if len(line) == 0:
                continue
            if line[0] == "exit":
                print("Thanks for using SnapFill shell!")
                sys.exit()
            elif line[0] == "help":
                shell_help()
            elif line[0] == "where":
                print("Branch: " + str(branch))
                print("Substring: " + str(substr))
            elif line[0] == "list" and len(line) > 1:
                if   line[1] == "branch":
                    conds = [(i, Synth.Program.cond_to_DSL(bp.conditions[i])) for i in range(len(bp.conditions))]
                    conds.append ((len(conds), "True"))
                    for c in conds:
                        print(str(c[0]) + ": " + c[1])
                    print()
                elif line[1] == "cond":
                    if branch == None:
                        print("Error: branch not set")
                        continue
                    if branch == len(snap_fill.conditions):
                        print("True")
                    for i in range(len(conds)):
                        print(str(i) + ": " + Synth.Program.cond_to_DSL(conds[i]))
                    print()
                elif line[1] == "substring":
                    if branch == None:
                        print("Error: branch not set")
                        continue
                    substrs = bp.progs[branch]
                    for i in range(len(substrs)):
                        if type(substrs[i]) == str:
                            s = "ConstStr(\"" + substrs[i] + "\")"
                        else:
                            lstr = Synth.DAG.SubstrExprVSA.pos_to_str(substrs[i][0])
                            rstr = Synth.DAG.SubstrExprVSA.pos_to_str(substrs[i][1])
                            s = "Substr(" + lstr + ", " + rstr + ")"
                        print(str(i) + ": " + s)
                elif line[1] == "start_pat":
                    if substr == None:
                        print("Error: substring not set")
                        continue
                    expr = snap_fill.progs[branch][substr]
                    if type(expr) == str:
                        print("0: ConstStr(\"" + expr + "\")")
                    else:
                        for i in range(len(starts)):
                            print(str(i) + ": " + Synth.DAG.SubstrExprVSA.pos_to_str(starts[i]))
                elif line[1] == "end_pat":
                    if substr == None:
                        print("Error: substring not set")
                        continue
                    expr = snap_fill.progs[branch][substr]
                    if type(expr) == str:
                        print("0: ConstStr(\"" + expr + "\")")
                    else:
                        for i in range(len(starts)):
                            print(str(i) + ": " + Synth.DAG.SubstrExprVSA.pos_to_str(ends[i]))
                else:
                    print("Unrecognized argument: " + line[1])
            elif line[0] == "set" and len(line) > 2 and line[2].isdigit():
                num = int(line[2])
                if   line[1] == "branch":
                    if num >=0 and num <= len(snap_fill.conditions):
                        if (branch != num):
                            substr = None
                            starts = None
                            ends = None
                        branch = num
                        if branch == len(snap_fill.conditions):
                            conds = None
                            continue
                        geq = [(True , pat, num) for (pat, num) in snap_fill.conditions[branch][0]]
                        lt  = [(False, pat, num) for (pat, num) in snap_fill.conditions[branch][1]]
                        conds = geq + lt
                    else:
                        print("Error: index out of bounds")
                elif line[1] == "substring":
                    if branch == None:
                        print("Error: branch not set")
                        continue
                    if num >= 0 and num < len(snap_fill.progs[branch]):
                        substr = num
                        ss = snap_fill.progs[branch][substr]
                        if type(ss) != str:
                            starts = snap_fill.pairs[branch][0].get_regexes(ss[0])
                            ends   = snap_fill.pairs[branch][0].get_regexes(ss[1])
                        else:
                            starts = None
                            ends = None
                    else:
                        print("Error: index out of bounds")
                else:
                    print("Unrecognized argument: " + line[1])
            elif line[0] == "change" and len(line) > 2 and line[2].isdigit():
                num = int(line[2])
                if   line[1] == "cond":
                    if conds == None or num >= len(conds):
                        print("Error: either this is the last branch or index out of bounds")
                        continue
                    bp.conditions[branch] = conds[num]
                elif line[1] == "start_pat":
                    if starts == None or num >= len(starts):
                        print("Error: substring is constant or index out of bounds")
                        continue
                    bp.progs[branch][substr] = (starts[num], bp.progs[branch][substr][1])
                elif line[1] == "end_pat":
                    if ends == None or num >= len(ends):
                        print("Error: substring is constant or index out of bounds")
                        continue
                    bp.progs[branch][substr] = (bp.progs[branch][substr][0], ends[num])
                else:
                    print("Unrecognized argument: " + line[1])
            elif line[0] == "print":
                print(bp.__str__())
            elif line[0] == "output":
                name = "snap.py"
                if len(line) > 1:
                    name = line[1]
                file = open(name, 'w')
                file.write(bp.to_python())
                file.close()
            elif line[0] == "eval":
                print("TODO")
            else:
                print("Error: command unrecognized or arguments lacking")
                print(raw)
                shell_help()
    sys.exit()
    
if __name__ == "__main__":
    main()
