#for info statments only:
import sys

import InputDataGraph as IDG
import DAG

class Synthesizer:
    """
    Synthesizer using IDG and DAG

    self.pairs      = list of (idg, dag) pairs
    self.inputs     = list of strings
    self.outputs    = list of strings
    self.pairs      = pairs of IDG and DAGs that cover the entire spec
    self.conditions = conditions to separate pairs (for now, just in the order that pairs originally is)
    """
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.pairs = []
        self.conditions = []
        self.original_idgs = None
        self.synthesize()

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
                    ranking_list.append((IDG.InputDataGraph.get_similarity(i,j),i[0],j[0]))
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
            self.conditions.append((geq_conds, lt_conds))

class SubstrExprEvaluator:
    """
    evaluator for a synthesized SubstrExpr

    self.left = start position
    self.right = end position
    -- position: an int (for a constant position) OR
            a tuple (regex index, count, Start/End [True = start, False = end])
    """
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def eval(self, in_str):
        """
        TODO: but basically just evaluate the substring
        """
        pass
    
