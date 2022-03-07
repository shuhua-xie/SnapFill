#for info statments only:
import sys

import InputDataGraph as IDG
import DAG

class Synthesizer:
    """
    Synthesizer using IDG and DAG

    self.pairs   = list of (idg, dag) pairs
    self.inputs  = list of strings
    self.outputs = list of strings, length <= inputs
    """
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.pairs = []
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
    
