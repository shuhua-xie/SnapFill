#for info statments only:
import sys

import InputDataGraph as IDG
import DAG
import Tokens as T

class Program:
    """
    for representing a singular program, i.e. the one that the Synthesizer generated

    self.conditions = conditions for each branch
        condition: (geq, pattern, num)
            geq     = True if the condition is >=, False if it is <
            pattern = regex pattern number, or string literal
            num     = match number
    self.progs      = program for each branch
    """
    def __init__(self, conds, ps):
        self.conditions = conds
        self.progs      = ps

    def __str__(self):
        """
        print DSL version of self
        """
        prog = "Switch{\n"
        for i in range(len(self.conditions)):
            cond = Program.cond_to_DSL(self.conditions[i])
            p    = Program.prog_to_DSL(self.progs[i])
            prog += "\t(" + cond + ", " + p + ")\n\n"
        p = Program.prog_to_DSL(self.progs[-1])
        prog += "\t(True, " + p + ")\n"
        prog += "}"
        return prog

    def size(self):
        # For switch
        sz = 1
        #for each condition
        sz += len(self.conditions) + 1
        for p in self.progs:
            # for Concat
            sz += 1
            for sub in p:
                # for Substr expressions
                sz += 1
                if type(sub) == str:
                    # for constant string expressions
                    sz += 1
                else:
                    # for position tuples
                    for pos in sub:
                        if type(pos) == int:
                            sz += 1
                        else:
                            sz += 4
        return sz

    def to_python(self):
        """
        returns string representing python program that can convert inputs

        returned program may fail if the input can't match as needed (index out of range errors)
        """
        prog  = "import sys\nimport re\nimport pandas as pd\nimport numpy as np\n\n"
        prog += "def snap(in_str):\n"
        x = "in_str"
        for i in range(len(self.conditions)):
            prog += Program.__cond_to_py(self.conditions[i]) + "\n"
            prog += Program.__prog_to_py(self.progs[i])
        prog += "\tif True:\n"
        prog += Program.__prog_to_py(self.progs[-1]) + "\n"

        # now write script part
        # input: will take a csv and fill in missing values
        help_str1  = "Useage: python3 snap.py [filename].csv"
        help_str2  = "Assumes: each line has at most 2 columns, optionally quoted by \\'s"
        help_str3  = "Output: file called snap-[filename].csv where each empty output column is filled"

        err  = "if len(sys.argv) < 2 or '.csv' not in sys.argv[1]:\n"
        err += "\tprint(\'" + help_str1 + "\')\n"
        err += "\tprint(\'" + help_str2 + "\')\n"
        err += "\tprint(\'" + help_str3 + "\')\n"
        err += "\tsys.exit()\n"

        iofunc  = "def getIO(path):\n"
        iofunc += "\tdata = pd.read_csv(path, dtype=str, header=None, quotechar=\"'\")\n"
        iofunc += "\tins = np.array(data[0]).tolist()\n"
        iofunc += "\tif len(list(data.columns)) < 2:\n"
        iofunc += "\t\touts = [float(\'NaN\')] * len(ins)\n"
        iofunc += "\telse:\n"
        iofunc += "\t\touts = np.array(data[1]).tolist()\n"
        iofunc += "\treturn ins, outs\n\n"

        prog += iofunc + err

        script  = "ins, outs = getIO(sys.argv[1])\n"
        script += "for i in range(len(outs)):\n"
        script += "\tif outs[i] != outs[i]:\n"
        script += "\t\touts[i] = snap(ins[i])\n"
        script += "\t\touts[i] = '---SynthError---' if not outs[i] else outs[i]\n\n"
        script += "li = re.split('[/\\\\\\\\]', sys.argv[1])\n"
        script += "li = [x for x in li if x]\n"
        script += "li[-1] = 'snap-' + li[-1]\n"
        script += "sep = '\\\\' if '\\\\' in sys.argv[1] else '/'\n"
        script += "name = sep.join(li)\n"
        script += "file = open(name, mode='w')\n"
        script += "for i in range(len(outs)):\n"
        script += "\tfile.write('\\\'' + ins[i]  + '\\\',')\n"
        script += "\tfile.write('\\\'' + outs[i] + '\\\'\\n')\n"
        script += "file.close()"
        return prog + script

    def eval_input(self, in_str):
        pass

    @staticmethod
    def prog_to_DSL(prog):
        """
        converts a program in to DSL string
        prog: list of substr/const string expressions
            if it's a string, it's a const string
            if it's a tuple, it's a substr

        each line is double tabbed (except for concat)
        """
        dsl = "Concat("
        for expr in prog:
            if type(expr) == str:
                dsl += "\n\t\tConstStr(\"" + expr + "\"),"
                continue
            lpos = expr[0]
            rpos = expr[1]
            lstr = DAG.SubstrExprVSA.pos_to_str(lpos)
            rstr = DAG.SubstrExprVSA.pos_to_str(rpos)
            dsl += "\n\t\tSubstr(" + lstr + ", " + rstr + "),"
        dsl += ")"
        return dsl

    @staticmethod
    def cond_to_DSL(cond):
        """
        converts a condition to DSL string
        """
        dsl = "Match(input, "
        if type(cond[1]) == str:
            dsl += "\"" + cond[1] + "\") "
        else:
            dsl += T.TOKENS[cond[1]] + ") "
        if cond[0]:
            dsl += ">= "
        else:
            dsl += "< "
        dsl += str(cond[2])
        return dsl

    @staticmethod
    def __prog_to_py(prog):
        """
        converts it to python
        note: each line is indented twice, there IS a newline at the end
        """
        py = "\t\tout_str = \"\"\n"
        for i in range(len(prog)):
            if type(prog[i]) == str:
                py += "\t\tout_str += \"" + prog[i] + "\"\n"
                continue
            left  = prog[i][0]
            right = prog[i][1]
            py += Program.__pos_to_safe_py(left, "l")
            py += Program.__pos_to_safe_py(right, "r")
            py += "\t\tout_str += in_str[l:r]\n"
        py += "\t\treturn out_str\n"
        return py

    @staticmethod
    def __pos_to_safe_py(pos, varname):
        """
        returns a program fragment, each line starts with 2 tabs, IS newline at end
        """
        if type(pos) == int:
            return "\t\t" + varname + " = " + str(pos - 1) + "\n"
        li = ""
        if type(pos[0]) == str:
            li += "list( re.compile( re.escape(\"" + pos[0] + "\") )"
        else:
            li += "list( " + str(T.MATCHERS[pos[0]])
        li += ".finditer(in_str) )"
        num = pos[1] - 1 if pos[1] > 0 else pos[1]
        length_req = pos[1] if pos[1] > 0 else abs(pos[1])
        py =  "\t\tli = " + li + "\n"
        py += "\t\tif len(li) < " + str(length_req) + ":\n\t\t\treturn None\n" 
        py += "\t\t" + varname + " = " + li + "[" + str(num) + "]"
        if pos[2]:
            py += ".start()\n"
        else:
            py += ".end()\n"
        return py

    @staticmethod
    def __cond_to_py(cond):
        """
        converts condition to python
        note: line indented once, no newline at the end
        """
        py = "\tif "
        if type(cond[1])== str:
            py += "len( re.compile(\"" + cond[1] + "\").findall(in_str) )"
        else:
            py += "len( " + str(T.MATCHERS[cond[1]]) + ".findall(in_str) )"
        if cond[0]:
            py += " >= "
        else:
            py += " < "
        py += str(cond[2]) + ":"
        return py

class Synthesizer:
    """
    Synthesizer using IDG and DAG

    self.error      = error string
    self.pairs      = list of (idg, dag) pairs
    self.inputs     = list of strings
    self.outputs    = list of strings
    self.pairs      = pairs of IDG and DAGs that cover the entire spec
    self.conditions = conditions to separate pairs (for now, just in the order that pairs originally is)
    self.progs      = list of ( list of SubStrVSAs that represent what to concat )
    self.best_prog  = Program instance
    """
    def __init__(self, inputs, outputs, flash):
        self.inputs = inputs
        self.outputs = outputs
        self.pairs = []
        self.conditions = []
        self.progs = None
        self.best_prog = None
        self.original_idgs = None
        self.error = None

        if flash:
            idgs = [IDG.InputDataGraph(self.inputs[i], i) for i in range(len(inputs))]
            idg_all = idgs[0]
            for i in idgs[1:]:
                idg_all = idg_all.intersect(i)
            dags = [DAG.DAG(self.inputs[i], self.outputs[i], i, idg_all) for i in range(len(outputs)) if self.outputs[i] == self.outputs[i]]
            if len(dags) == 0:
                self.error = "No valid examples"
                return
            dag_all = dags[0]
            for d in dags[1:]:
                dag_all = dag_all.intersect(d)
            if not dag_all.has_solution(self.outputs):
                self.error = "No solution found"
                return
            self.pairs = [(idg_all, dag_all)]
            self.conditions = []
        else:
            self.synthesize()
        if not self.error:
            self.gen_program()

    def synthesize(self):
        """
        Build the DAG (do the synthesis)
        """
        for i in range(len(self.inputs)):
            currIDG = IDG.InputDataGraph(self.inputs[i],i)
            currDAG = None
            if (self.outputs[i] == self.outputs[i]):
                currDAG = DAG.DAG(self.inputs[i],self.outputs[i],i, currIDG)
            self.pairs.append((currIDG, currDAG))
        self.original_idgs = [idg for (idg, dag) in self.pairs]
        
        # combining IDG without outputs to those with outputs
        while(None in list(zip(*self.pairs))[1]):
            PairsWithOutput = [self.pairs[i] for i in range(len(self.pairs)) if self.pairs[i][1] != None]
            PairsWithoutOutput = [self.pairs[i] for i in range(len(self.pairs)) if self.pairs[i][1] == None]
            
            ranking_list = []
            for i in PairsWithoutOutput:
                for j in PairsWithOutput:
                    # ranking_list = list of (similarity: float, IDG1, IDG2) tuples
                    ranking_list.append((IDG.InputDataGraph.get_similarity(i[0], j[0]),i[0],j[0]))
            ranking_list.sort(reverse=True)
            merged = False
            
            for pair in ranking_list:
                newIDG = pair[1].intersect(pair[2])
                if newIDG.size() == 0:
                    continue
                
                ids = next(iter(newIDG.nodes)).ids()
                newDAGS = [DAG.DAG(self.inputs[i], self.outputs[i], i , newIDG) for i in ids if self.outputs[i] == self.outputs[i]]
                newDAG = newDAGS[0]
                for dag in newDAGS[1:]:
                    newDAG = newDAG.intersect(dag)
                if newDAG.has_solution(self.outputs):
                    tempPairs = [p for p in self.pairs if (p[0] != pair[1] and p[0] != pair[2])]
                    tempPairs.append((newIDG, newDAG))
                    self.pairs = tempPairs
                    merged = True
                    break
            if not merged:
                self.pairs = None
                self.error = "Some inputs could not be taken into account\n"
                return
        # End while loop 1

        merged = True
        while(merged):
            merged = False
            
            ranking_list = []
            for i in range(len(self.pairs) - 1):
                for j in range(i+1, len(self.pairs)):
                    idg1 = self.pairs[i][0]
                    idg2 = self.pairs[j][0]
                    ranking_list.append((IDG.InputDataGraph.get_similarity(idg1, idg2), idg1, idg2))
            ranking_list.sort(reverse=True)
            
            for pair in ranking_list:
                newIDG = pair[1].intersect(pair[2])
                if newIDG.size() == 0:
                    continue
                
                ids = next(iter(newIDG.nodes)).ids()
                newDAGS = [DAG.DAG(self.inputs[i], self.outputs[i], i , newIDG) for i in ids if self.outputs[i] == self.outputs[i]]
                newDAG = newDAGS[0]
                for dag in newDAGS[1:]:
                    newDAG = newDAG.intersect(dag)
                if newDAG.has_solution(self.outputs):
                    tempPairs = [p for p in self.pairs if (p[0] != pair[1] and p[0] != pair[2])]
                    tempPairs.append((newIDG, newDAG))
                    self.pairs = tempPairs
                    merged = True
                    break
        # End while loop 2

    def learn_conditions(self):
        """
        learn condition pairs for the branches (sorts the branches, so conditions match with branches in order)

        self.conditions = list of (>= conditions, < conditions)
            patterns in the branch IDG and not in any of the original idgs of ids not in the branch are >= conditions
            patterns not in any original idg of ids in the branch but in all other branches are < conditions

        conditions can be simplified:
            >= conditions: only keep the positive ones, and only keep the patterns with the largest match number
            <  conditions: only keep the positive ones, and only keep the patterns with the smallest match number
        """
        self.pairs.sort(key=lambda p: len( next(iter(p[0].nodes)).ids() ) )
        covered = set()
        for i in range(len(self.pairs) - 1):
            idg = self.pairs[i][0]
            ids = next(iter(idg.nodes)).ids()
            positive_union = set()
            for pos_id in ids:
                positive_union = positive_union.union(self.original_idgs[pos_id].patterns)
            covered = covered.union(set(ids))
            negative_union = set()
            for neg_id in range(len(self.original_idgs)):
                if neg_id not in covered:
                    negative_union = negative_union.union(self.original_idgs[neg_id].patterns)
            geq_conds = idg.patterns.difference(negative_union)

            negative_idgs = [self.pairs[j][0] for j in range(i+1, len(self.pairs))]
            negative_intersection = negative_idgs[0].patterns
            for neg_idg in negative_idgs[1:]:
                negative_intersection = negative_intersection.intersection(neg_idg.patterns)
            lt_conds = negative_intersection.difference(positive_union)

            # simplify conditions
            geq_conds = {(pat, num) for (pat, num) in geq_conds if num > 0}
            tmp = dict()
            for pat, num in geq_conds:
                tmp.setdefault(pat, num)
                if tmp[pat] < num:
                    tmp[pat] = num
            geq_conds = set(tmp.items())
            lt_conds  = {(pat, num) for (pat, num) in lt_conds  if num > 0}
            tmp = dict()
            for pat, num in lt_conds:
                tmp.setdefault(pat, num)
                if tmp[pat] > num:
                    tmp[pat] = num
            lt_conds = set(tmp.items())
            if not geq_conds and not lt_conds:
                self.error = "Conditions could not be generated\n"
                return
            self.conditions.append((geq_conds, lt_conds))

    def gen_program(self):
        """
        Generate the program
        """
        self.progs = []
        for idg, dag in self.pairs:
            idg.rank_nodes()
            self.progs.append(dag.best_solution(idg, self.outputs))

        self.learn_conditions()
        conds = []
        for geq, lt in self.conditions:
            c_set = geq
            geq = True
            if not c_set:
                c_set = lt
                geq = False
            re_li = [(pat, num) for (pat, num) in c_set if type(pat) == int]
            if not re_li:
                re_li = [(pat, num) for (pat, num) in c_set if type(pat) == str]
                re_li.sort(key=lambda p: len(p[0]), reverse=True)
            else:
                re_li.sort(key=lambda p: p[0], reverse=True)
            conds.append((geq, re_li[0][0], re_li[0][1]))

        chosen_ps = []
        for i in range(len(self.progs)):
            # p is a result of dag.best_solution(), i.e. a list of constants and node pairs
            p = self.progs[i]
            chosen = []
            for expr in p:
                if type(expr) == str:
                    chosen.append(expr)
                    continue
                lpos = expr[0]
                if type(lpos) != int:
                    l_res = self.pairs[i][0].get_regexes(lpos)
                    l_res.sort(key=lambda t: t[0] if type(t[0]) == int else -3, reverse=True)
                    lpos = l_res[0]
                rpos = expr[1]
                if type(rpos) != int:
                    r_res = self.pairs[i][0].get_regexes(rpos)
                    r_res.sort(key=lambda t: t[0] if type(t[0]) == int else -3, reverse=True)
                    rpos = r_res[0]
                chosen.append( (lpos, rpos) )
            chosen_ps.append(chosen)
        self.best_prog = Program(conds, chosen_ps)
