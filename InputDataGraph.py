import re
import Tokens as T

#NOTE: current implementation limitations:
#       - only considering single column inputs
class InputDataGraph:
    """
    InputDataGraph class

    nodes: set of tuples representing the labels of each node
        - set because order doesn't matter
        - tuples because order of indices does matter, but sets cannot contain lists
    edges: dictionary mapping from (node1, node2) to a set of matching regex
                where each regex match is (pattern, match_number)
                pattern: a string literal or an integer constant indicating the pattern type
        - dictionary for fast lookup
        - tuples since it is a dictionary
    """

    def __str__(self):
        ret = "nodes: " + self.nodes.__str__()
        for k in self.edges.keys():
            li = "{"
            for (re, num) in self.edges[k]:
                if type(re) == int:
                    li += " (" + T.TOKENS[re]
                else:
                    li += " (\"" + re + "\""
                li += ", " + num.__str__() + "),"
            li += "}"
            ret += "\n" + k.__str__() + ": " + li
        return ret

    def __init__(self, in_str, prev_graph = None):
        """
        Create a InputDataGraph based on one input string and intersect with the graph of all previous strings
    
        in_str:     the next line of input as a string
        prev_graph: the intersection of the InputDataGraphs of all the previous strings, defaults to None
        """
        self.nodes = set()
        self.edges = dict()
        self.__generate_graph__(in_str)
        if (prev_graph):
            self.intersect(prev_graph)

    def __generate_graph__(self, in_str):
        """
        first function called when generating an InputDataGraph, creates the graph for a single input

        assumes:  nodes and edges are empty, in_str is nonempty
        returns:  nothing
        modifies: fills in nodes and edges as specified
        """
        # don't label with id since id can be implied by position in list
        for i in range(0, len(in_str) + 3):
            self.nodes.add((i))
        # set ^ and $ first
        self.edges[((0,), (1,))] = set()
        self.edges[((0,), (1,))].add((-2, 1))
        self.edges[((len(in_str) + 1,), (len(in_str) + 2,))] = set()
        self.edges[((len(in_str) + 1,), (len(in_str) + 2,))].add((-1, 1))

        # attempt to match each regex on the input
        for i in range(0, len(T.MATCHERS)):
            ind = 0
            total_matches = len(T.MATCHERS[i].findall(in_str))
            for m in T.MATCHERS[i].finditer(in_str):
                ind += 1
                label = ((m.start() + 1,), (m.end() + 1,))
                self.edges.setdefault(label, set())
                # add (regex pattern number, match number)
                self.edges[label].add((i, ind))
                # add negative match number as well
                self.edges[label].add((i, -1 * total_matches + ind - 1))

        # add constant labels
        for i in range(1, len(in_str) + 1):
            for j in range (i + 1, len(in_str) + 2):
                label = ((i,), (j,))
                self.edges.setdefault(label, set())
                c_str = in_str[i - 1: j - 1]
                # find the match number of this constant string
                c_match = re.compile(c_str)
                ind = len(c_match.findall(in_str, 0, i - 1 + len(c_str)))
                neg_ind = -1 * len(c_match.findall(in_str, i - 1))
                self.edges[label].add((c_str, ind))
                self.edges[label].add((c_str, neg_ind))

    def intersect(self, other):
        """
        calculates the intersection between this graph and other, storing the result in this graph
        other: the other InputDataGraph

        assumes: neither self nor other are empty
        returns: nothing
        modifies: self.nodes and self.edges to intersect with other.nodes and other.edges
            - the index labels of self.nodes will be at the end of the intersected node labels
            - ^^^ is important for ordering
        """
        # general prodcedure:
        #   create temporary edge and node variables to store intersection
        #   intersect edge labels
        #   if non-empty, then add the nodes and the edge
        new_nodes = set()
        new_edges = dict()
        for s_edge_key in self.edges.keys():
            for o_edge_key in other.edges.keys():
                common = set.intersection(self.edges[s_edge_key], other.edges[o_edge_key])
                if common:
                    n1 = o_edge_key[0] + s_edge_key[0]
                    n2 = o_edge_key[1] + s_edge_key[1]
                    new_nodes.add(n1)
                    new_nodes.add(n2)
                    # TODO: is this correct? Are nodes guaranteed not to repeat?
                    new_edges[(n1, n2)] = common
        self.nodes = new_nodes
        self.edges = new_edges

