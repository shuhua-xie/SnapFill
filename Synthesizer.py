#for info statments only:
import sys

import InputDataGraph as IDG
import DAG

class Synthesizer:
    """
    Synthesizer using IDG and DAG

    self.synth_IDG     = input data graph using all of the inputs
    self.synth_DAG     = DAG using the IDG and all outputs
    self.inputs  = list of strings
    self.outputs = list of strings, length <= inputs
    """
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.PAIRS = []
        self.synthesize()

    def synthesize(self):
        """
        Build the DAG (do the synthesis)
        """
        
        print("---info--- building InputDataGraph", file=sys.stderr)
        for i in range(len(self.inputs)):
            currIDG = IDG.InputDataGraph(self.inputs[i],i)
            if (self.outputs[i] == self.outputs[i]):
                currDAG = DAG.DAG(self.inputs[i],self.outputs[i],i, currIDG)
                self.PAIRS.append((currIDG, currDAG))
            else:
                self.PAIRS.append((currIDG, None))
        
        
        # combining IDG without outputs to those with outputs
        while(None in list(zip(*self.PAIRS))[1]):
            
            IDGWithOutput = [self.PAIRS[i] for i in range(len(self.PAIRS)) if self.PAIRS[i][1] != None]
            IDGWithoutOutput = [self.PAIRS[i] for i in range(len(self.PAIRS)) if self.PAIRS[i][1] == None]
            
            ranking_list = []
            
            for i in IDGWithoutOutput:
                for j in IDGWithOutput:
                    ranking_list.append((IDG.get_similarity(i,j),i[0],j[0]))
                    
            ranking_list.sort()
            
            merged = False
            
            for pair in ranking_list:
                
                newIDG = pair[1].intesect(pair[2])
                
                if newIDG.size() == 0:
                    continue
                
                ids = next(iter(newIDG.nodes)).ids()
                
                newDAGS = []
                
                for i in ids:
                    if self.outputs[i] == self.outputs[i]:
                        newDAGS.append(DAG.DAG(self.inputs[i],self.outputs[i],i, newIDG))
                
                newDAG = newDAGS[0]
                for dag in newDAGS[1:-1]:
                    newDAG = newDAG.intersect(dag)
                
                
                if newDAG.has_solution(self.outputs):
                    tempPairs = []
                    for i in self.PAIRS:
                        if idFirst != next(iter(i[0].nodes)).ids() and idSecond != next(iter(i[0].nodes)).ids():
                            tempPairs.append(i)

                    tempPairs.append((newIDG, newDAG))

                    self.PAIRS = tempPairs
                    
                    merged = True
                    
                    break
                    
            if not merged:
                return None
                
                             
        print("---info--- DAG built", file=sys.stderr)

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
    
