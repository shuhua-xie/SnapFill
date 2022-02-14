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
        self.synth_IDG = None
        self.synth_DAG = None
        self.inputs = inputs
        self.outputs = outputs
        self.synthesize()

    def synthesize(self):
        """
        Build the DAG (do the synthesis)
        """
        for i in self.inputs:
            self.synth_IDG = IDG.InputDataGraph(i, self.synth_IDG)
        for ind in range(len(self.outputs)):
            self.synth_DAG = DAG.DAG(self.inputs[ind], 
                                     self.outputs[ind],
                                     ind, self.synth_IDG, self.synth_DAG)

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
    
