# DAG.py
# DAG and its related classes

# NOTE:
#   want DAG to represent many possible solutions
#   maybe?? also want some class to represent a single solution
#       - this class can then be "compiled" to python and returned to the user or run on other input

import InputDataGraph as IDG

class DAG_Edge:
    """
    An edge of a DAG

    substr: tuple of two sets of positions
        each set contains nodes labels from input_graph that correspond to the position
    c_str: const string expression
    """
    def __init__(self, substr, input_graph, input_string, str_ind):

class DAG:
    """
    DAG class

    nodes: set of node labels
    edges: dictionary mapping pairs of node labels to DAG_Edge objects
    """
    def __init__(self, out_str, input_graph, pre_DAG = None):

    def __generate_graph__():

    def intersect(self, other):


