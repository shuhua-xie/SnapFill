import re
from copy import copy
import Tokens as T
from common import *

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

    def __init__(self, in_str, ind):
        """
        Create a InputDataGraph based on one input string and intersect with the graph of all previous strings
    
        in_str:     the next line of input as a string
        prev_graph: the intersection of the InputDataGraphs of all the previous strings, defaults to None
        """
        self.nodes = set()
        self.edges = dict()
        self.__generate_graph__(in_str, ind)

    def __generate_graph__(self, in_str, ind):
        """
        first function called when generating an InputDataGraph, creates the graph for a single input

        assumes:  nodes and edges are empty, in_str is nonempty
        returns:  nothing
        modifies: fills in nodes and edges as specified
        """
        for i in range(0, len(in_str) + 3):
            self.nodes.add(NodeLabel( ((ind, i),) ))
        fst_node  = NodeLabel( ((ind, 0),) )
        snd_node  = NodeLabel( ((ind, 1),) )
        snd_last_node  = NodeLabel( ((ind, len(in_str) + 1),) )
        last_node = NodeLabel( ((ind, len(in_str) + 2),) )
        # set ^ and $ first
        self.edges[(fst_node, snd_node)] = set()
        self.edges[(fst_node, snd_node)].add((-2, 1))
        self.edges.setdefault((snd_last_node, last_node), set())
        self.edges[(snd_last_node, last_node)].add((-1, 1))

        # attempt to match each regex on the input
        for i in range(0, len(T.MATCHERS)):
            ind = 0
            total_matches = len(T.MATCHERS[i].findall(in_str))
            for m in T.MATCHERS[i].find
            (in_str):
                ind += 1
                s = NodeLabel( ((ind, m.start() + 1),) )
                f = NodeLabel( ((ind, m.end()   + 1),) )
                label = (s, f)
                #label = ((m.start() + 1,), (m.end() + 1,))
                self.edges.setdefault(label, set())
                # add (regex pattern number, match number)
                self.edges[label].add((i, ind))
                # add negative match number as well
                self.edges[label].add((i, -1 * total_matches + ind - 1))

        # add constant labels
        for i in range(1, len(in_str) + 1):
            for j in range (i + 1, len(in_str) + 2):
                s = NodeLabel( ((ind, i),) )
                f = NodeLabel( ((ind, j),) )
                label = (s, f)
                #label = ((i,), (j,))
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
        temp = copy(self)
        new_nodes = set()
        new_edges = dict()
        for s_edge_key in self.edges.keys():
            for o_edge_key in other.edges.keys():
                common = set.intersection(self.edges[s_edge_key], other.edges[o_edge_key])
                if common:
                    n1 = NodeLabel.join(o_edge_key[0], s_edge_key[0])
                    n2 = NodeLabel.join(o_edge_key[1], s_edge_key[1])
                    new_nodes.add(n1)
                    new_nodes.add(n2)
                    new_edges[(n1, n2)] = common
        temp.nodes = new_nodes
        temp.edges = new_edges
        return temp
    
    def size(self):
        return len(self.edges.keys())
    
    def __lt__(self, other):
        return (self.size() < other.size())
    
    @staticmethod
    def get_similarity(IDG1, IDG2):
        """
        returns similarity of two IDGs
        assumes: IDG1 and IDG2 are in fact IDGs
        """
        size1 = IDG1.size()
        size2 = IDG2.size()
        tempIDG = IDG1.intersect(IDG2)
    
        sizeNew = tempIDG.size()
    
        return float(sizeNew)/(size1+size2)
