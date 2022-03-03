from copy import copy

import InputDataGraph as IDG
from InputDataGraph import re
from InputDataGraph import T
from common import *

class SubstrExprVSA:
    """
    Substring Expression VSA: represents an entire set of Substring expressions
        as can be defined from Figure 10a of the FlashFill paper

    constant: bool representing whether it's the constant string expression
    if constant == TRUE
        val: the value of the constant substring
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
        lset = "set("
        for p in self.pl:
            lset += p.__str__() + ", "
        lset += ")"
        rset = "set("
        for p in self.pr:
            rset += p.__str__() + ", "
        rset += ")"
        ret += "left = "  + lset + "\n"
        ret += "right = " + rset + "\n"
        return ret

    def __init__(self, cons, val = None, pl = None, pr = None):
        self.constant = cons
        self.val = val
        self.pl = pl
        self.pr = pr

    def print_progs(self, idg):
        """
        Print the programs represented by this SubstrExpr

        requires:
        idg: Input Data Graph used to construct the DAG that this SubstrExpr appears in
        """
        if self.constant:
            print("ConstantStr(\"" + self.val + "\")")
            return
#        print("Substrings (where regex tokens are represented as (regex, match number, direction))\n")
        for l in self.pl:
            for r in self.pr:
                l_pos_li = [l] if (type(l) == int) else self.__get_regexes(l, idg)
                r_pos_li = [r] if (type(r) == int) else self.__get_regexes(r, idg)
                for l_pos in l_pos_li:
                    for r_pos in r_pos_li:
                        print("SubStr(input, " + 
                                self.__pos_to_str(l_pos) + 
                                ", " + 
                                self.__pos_to_str(r_pos) + ")")
    
    def __get_regexes(self, node_label, idg):
        """
        get regexes matching node label

        assumes: node_label is valid, idg is the IDG used for the DAG this SubstrExpr is a part of
        returns: list of tuples of form (regex id OR literal, position, Dir [True for Start, False for End])
        """
        ret = []
        for e_key in idg.edges.keys():
            if e_key[0] == node_label or e_key[1] == node_label:
                dir = e_key[0] == node_label
                for (r, num) in idg.edges[e_key]:
                    ret.append( (r, num, dir) )
        return ret

    @staticmethod
    def __pos_to_str(pos):
        """
        input: either an int or a position as returned in __get_regexes()
        returns: the string for of the int
              OR a string form of the tuple
        """
        if type(pos) == int:
            return str(pos)
        ret = "input.match("
        if type(pos[0]) == str:
            ret += "\"" + pos[0] + "\", "
        else:
            ret += T.TOKENS[pos[0]] + ", "
        ret += str(pos[1]) + ", "
        if pos[2]:
            ret += "Start)"
        else:
            ret += "End)"
        return ret


    @staticmethod
    def intersect(obj1, obj2):
        if (not isinstance(obj1, SubstrExprVSA) or
            not isinstance(obj2, SubstrExprVSA) or
             obj2.constant != obj2.constant      ):
            return None

        # both are constant values
        if obj1.constant and obj1.val == obj2.val:
            return SubstrExprVSA(obj1.constant, obj1.val, None, None)
        if not obj1.constant and not obj2.constant:
            new_pl = obj1.pl.intersection(obj2.pl)
            new_pr = obj1.pr.intersection(obj2.pr)
            if new_pl and new_pr:
                return SubstrExprVSA(obj1.constant, None, new_pl, new_pr)
        return None

class DAG:
    """
    DAG generation class

    nodes: set of NodeLabels representing the labels of each node
    edges: dictionary mapping from (NodeLabel1, NodeLabel2) to a set of substring expressions
                where each substring expression is (v_l, v_r, constant string)
                v_l, v_r = independent sets of position expressions
    """
    def __str__(self):
        nodestr = "set("
        for n in self.nodes:
            nodestr += n.__str__() + ", "
        nodestr += ")"
        ret = "nodes: " + nodestr + "\n"
        for k in self.edges.keys():
            li = ""
            for substr in self.edges[k]:
                li += substr.__str__() + "\n"
            ret += "---" + k[0].__str__() +  " to " + k[1].__str__() + ":\n{" + li + "}" + "\n\n"
        return ret

    def __init__(self, input_str, output_str, example_ind, input_graph):
        """
        create a DAG for each input-output example and intersect with the DAG of all previous examples

        input_str: input example as string
        output_str: corresponding output example as substring
        example_ind: the index of the example, for looking up indices in IDG node labels
                    (serves as id for DAG node labels)
        input_graph: InputDataGraph generated from the whole dataset
        prev_DAG: intersection of the DAGs of all previous examples, defaults to None
        """

        self.nodes = set()
        self.edges = dict()
        self.generate_DAG(input_str, output_str, example_ind, input_graph)

    def generate_DAG(self, input_str, output_str, example_ind, input_graph):
        """
        first function called when generating a DAG, creates the graph for a single input-output example

        assumes:  nodes and edges are empty, input_str is non-empty
        returns:  nothing
        modifies: fills in nodes and edges as specified
        """
        # create len(output_str) + 1 number of nodes and a start node with label 0
        # since nodes are the spaces between letters
        nodes_li = []
        for i in range(1, len(output_str) + 2):
            nodes_li.append(NodeLabel( ((example_ind ,i),) ))
#            self.nodes.add((i,))
        self.nodes = set(nodes_li)

        # Iterate over all substrings output_str[i..j] of the output string and add an edge (i,j) between the labels i and j
        for i in range(0, len(nodes_li) - 1):
            for j in range(i + 1, len(nodes_li)):
                label = (nodes_li[i], nodes_li[j])
                self.edges.setdefault(label, set())
                substr = output_str[i:j]
                
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

    def intersect(self,other):
        """
        calculates the intersection between this graph and other, storing the result in this graph
        --> NOT an idempotent operation
        other: the other DAG

        assumes: neither self nor other are empty 
            ^ actually, it should work just fine even if they are
        returns:  a new DAG
        modifies: self.nodes and self.edges to intersect with other.nodes and other.edges
            - the index labels of self.nodes will be at the end of the intersected node labels
            - ^^^ is important for ordering
        """
        ret = copy(self)
        new_nodes = set()
        new_edges = dict()
        for s_edge_key in self.edges.keys():
            for o_edge_key in other.edges.keys():

                # find common nodes of both independent sets respectively
                common = set()
                # for correctness, must attempt to intersect every substr expr with every other
                for substr_expr1 in self.edges[s_edge_key]:
                    for substr_expr2 in other.edges[o_edge_key]:
                        intersection = SubstrExprVSA.intersect(substr_expr1, substr_expr2) 
                        if intersection:
                            common.add(intersection)

                if common:
                    n1 = NodeLabel.join(o_edge_key[0], s_edge_key[0])
                    n2 = NodeLabel.join(o_edge_key[1], s_edge_key[1])
                    new_nodes.add(n1)
                    new_nodes.add(n2)
                    new_edges[(n1, n2)] = common
        ret.nodes = new_nodes
        ret.edges = new_edges
        return ret

    def has_solution(self, outputs):
        """
        returns whether or not there is a path through the DAG 

        outputs: list of ALL outputs in consideration (will be used to look up based on index)
        """
        if (not self.nodes):
            return False
        ids = next(iter(self.nodes)).ids()
        lengths = [len(s) + 1 for s in outputs]
        goal = tuple( [l for (i,l) in set(zip(range(len(lengths)), lengths)) if i in ids] )
        start = tuple(1 for x in range(len(ids)))

        e = dict()
        for (in_l, out_l) in self.edges.keys():
            e.setdefault(in_l.inds(), set())
            e[in_l.inds()].add(out_l.inds())
        reach = set()
        reach.add(start)
        horizon = e[start]
        while not horizon <= reach:
            reach = set.union(reach, horizon)
            new_horizon = set()
            for item in horizon:
                if item in e:
                    new_horizon = set.union(new_horizon, e[item])
            horizon = new_horizon
        return goal in reach

