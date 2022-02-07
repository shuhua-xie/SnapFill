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
        """
        learn the DAG edge label for some substring

        substr: the string to learn programs for
        input_graph: IDG of all inputs
        input_str: the input for the given output substring
        str_ind: index of the input output pair in question
        """

    def intersect(self, other):
        """
        intersect this DAG_Edge with another
        """

class DAG:
    """
    DAG class

    nodes: set of node labels
    edges: dictionary mapping pairs of node labels to DAG_Edge objects
    """
    def __init__(self, out_str, str_ind, input_graph, input_strings, prev_DAG = None):
        """
        create DAG for output string given and intersect with previous DAG

        out_str: output string
        str_ind: index of the output string (used to find correct position in IDG)
        input_graph: IDG of all inputs
        input_strings: list of strings
        prev_DAG: intersected DAG of all previous inputs
        """
        self.nodes = set()
        self.edges = dict()
        self.__generate_graph__()
        if prev_DAG:
            self.intersect(prev_DAG)

    def __generate_graph__(self, out_str, str_ind, input_graph, input_strings):
        """
        generate DAG for 1 output
        """
        for i in range(0, len(out_str) + 1):
            self.nodes.add((i,))
        # generate edges
        for i in range(0, len(out_str)):
            for j in range(i, len(out_str) + 1):
                self.edges[((i,), (j,))] = DAG_Edge(outstr[i:j], input_graph, input_strings[str_ind], str_ind)

    def intersect(self, other):
        """
        intersect this DAG with 'other' DAG
        """


