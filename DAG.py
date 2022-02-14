import InputDataGraph as IDG
from InputDataGraph import re

class SubstrExprVSA:
    """
    Substring Expression VSA: represents an entire set of Substring expressions
        as can be defined from Figure 10a of the FlashFill paper

    constant: bool representing whether it's the constant string expression
    if constant == TRUE
        s: the value of the constant substring
    if constant == FALSE
        pl: set of positions representing the left
        pr: set of positions representing the right
        -- TENTATIVELY: position corresponding to regex = tuple (IDG node label)
                        position corresponding to constant position = integer
    """
    def __str__(self):
        if self.constant:
            return "ConstantStr(\"" + self.val + "\")\n"
        ret  = "Substr(left, right)\n"
        ret += "left = "  + self.pl.__str__() + "\n"
        ret += "right = " + self.pr.__str__() + "\n"
        return ret

    def __init__(self, cons, val = None, pl = None, pr = None):
        self.constant = cons
        self.val = val
        self.pl = pl
        self.pr = pr

    @staticmethod
    def intersect(obj1, obj2):
        if (not isinstance(obj1, SubstrExprVSA) or
            not isinstance(obj2, SubstrExprVSA) or
             self.constant != other.constant      ):
            return None

        # both are constant values
        if obj1.constant and sbj1.val == obj2.val:
            return SubstrExprVSA(obj1.constant, obj1.val, None, None)
        if not self.constant:
            new_pl = obj1.pl.intersection(obj2.pl)
            new_pr = obj1.pr.intersection(obj2.pr)
            if new_pl and new_pr:
                return SubstrExprVSA(obj1.constant, None, new_pl, new_pr)
        return None

class DAG:
    """
    DAG generation class

    nodes: set of tuples representing the labels of each node
    edges: dictionary mapping from (node1, node2) to a set of substring expressions
                where each substring expression is (v_l, v_r, constant string)
                v_l, v_r = independent sets of position expressions
    """
    def __str__(self):
        ret = "nodes: " + self.nodes.__str__() + "\n"
        for k in self.edges.keys():
            li = ""
            for substr in self.edges[k]:
                li += substr.__str__() + "\n"
            ret += ">>>" + k.__str__() + ":\n{" + li + "}" + "\n\n"
        return ret

    def __init__(self, input_str, output_str, example_ind, input_graph, prev_DAG = None):
        """
        create a DAG for each input-output example and intersect with the DAG of all previous examples

        input_str: input example as string
        output_str: corresponding output example as substring
        example_ind: the index of the example, for looking up indices in IDG node labels
        input_graph: InputDataGraph generated from the whole dataset
        prev_DAG: intersection of the DAGs of all previous examples, defaults to None
        """

        self.nodes = set()
        self.edges = dict()
        self.generate_DAG(input_str, output_str, example_ind, input_graph)
        if prev_DAG:
            self.intersect(prev_DAG)

    def generate_DAG(self, input_str, output_str, example_ind, input_graph):
        """
        first function called when generating a DAG, creates the graph for a single input-output example

        assumes:  nodes and edges are empty, input_str is non-empty
        returns:  nothing
        modifies: fills in nodes and edges as specified
        """
        # get start index and end index of output string in input string
#        match = re.finditer(output_str, input_str)
#        start_index = match.start()
#        end_index = match.end()

        # create len(output_str) + 1 number of nodes and a start node with label 0
        # since nodes are the spaces between letters
        for i in range(1, len(output_str) + 2):
            self.nodes.add((i,))

        # Iterate over all substrings output_str[i..j] of the output string and add an edge (i,j) between the labels i and j
        for i in range(0, len(output_str)):
            for j in range(i + 1, len(output_str) + 1):
                label = ((i+1,), (j+1,))
                self.edges.setdefault(label, set())
                substr = input_str[i:j]
                
                # add constant expr
                self.edges[label].add(SubstrExprVSA(True, substr, None, None))

                # want to search for each occurence of substring in input
                # each occurence becomes a SubstrExprVSA
                for m in re.finditer(substr, input_str):
                    l = m.start() + 1
                    r = m.end() + 1
                    vl = set()
                    vr = set()
                    vl.add(l)
                    vr.add(r)
                    for v in input_graph.nodes:
                        if v[example_ind] == l:
                            vl.add(v)
                        elif v[example_ind] == r:
                            vr.add(v)
                    self.edges[label].add(SubstrExprVSA(False, None, vl, vr))

                # create two independent sets of position expressions v_l and v_r
                # a set of position expression consists of a set of IDG nodes and a constant position
#                v_l, v_r = set()
#                for v in input_graph.nodes:
#                    if i in v:
#                        v_l.add(v)
#                    if j in v:
#                        v_r.add(v)

                # add constant position to v_l and v_r
#                v_l.add(i)
#                v_r.add(j)

                # add independent sets of IDG nodes and constant string for given substring
#                self.edges[label].add(v_l, v_r, substr)

    def intersect(self,other):
        """
        calculates the intersection between this graph and other, storing the result in this graph
        --> NOT an idempotent operation
        other: the other DAG

        assumes: neither self nor other are empty 
            ^ actually, it should work just fine even if they are
        returns: nothing
        modifies: self.nodes and self.edges to intersect with other.nodes and other.edges
            - the index labels of self.nodes will be at the end of the intersected node labels
            - ^^^ is important for ordering
        """
        new_nodes = set()
        new_edges = dict()
        for s_edge_key in self.edges.keys():
            for o_edge_key in other.edges.keys():

                # find common nodes of both independent sets respectively
#                common = set.intersection(self.edges[s_edge_key][0], other.edges[o_edge_key][0])
#                common_vr = set.intersection(self.edges[s_edge_key][1], other.edges[o_edge_key][1])
#                if common_vr:
#                    common.add(common_vr)
#                common_str = set.intersection(self.edges[s_edge_key][2], other.edges[o_edge_key][2])
#                if common_str:
#                    common.add(common_str)
                common = set()
                # for correctness, must attempt to intersect every substr expr with every other
                for substr_expr1 in self.edges[s_edge_key]:
                    for substr_expr2 in other.edges[s_edge_key]:
                        intersection = SubstrExprVSA.intersect(substr_expr1, substr_expr2) 
                        if intersection:
                            common.add(intersection)

                if common:
                    n1 = o_edge_key[0] + s_edge_key[0]
                    n2 = o_edge_key[1] + s_edge_key[1]
                    new_nodes.add(n1)
                    new_nodes.add(n2)
                    new_edges[(n1, n2)] = common
        self.nodes = new_nodes
        self.edges = new_edges
