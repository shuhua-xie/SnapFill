import bisect

import InputDataGraph as IDG
from InputDataGraph import re
from InputDataGraph import T

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
        ret += "left = "  + self.pl.__str__() + "\n"
        ret += "right = " + self.pr.__str__() + "\n"
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

class DAGNodeLabel:
    """
    represents the label of a DAG node
    is a tuple of tuples, the outer one maintains a sorted property
        inner ones are pairs, representing (id, index)

    label: tuple of tuples

    supported operations: 
    DAGNodeLabel.join(), joins two node labels into 1, assumes the two label's ids are disjoint
    self.indexof(), given id, returns the index or None
    """
    def __init__(self, label):
        self.label = label

    def __eq__(self, other):
        if isinstance(other, DAGNodeLabel):
            return self.label == other.label
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.label.__str__()

    def __hash__(self):
        return hash(self.label)

    def indexof(self, ind):
        """
        input: an id (int)
        output: corresponding id's index (or None if it isn't present)
        """
        ids, inds = tuple(zip(*self.label))
        expect_i = bisect.bisect_left(ids, ind)
        if (expect_i == len(ids) or ids[expect_i] != ind):
            return None
        return inds[expect_i]

    @staticmethod
    def join(label1, label2):
        """
        assumes, label1 and label2 are valid
        returns: new label containing all pairs in both original labels
        """
        if (len(label1.label) == 0):
            return label2
        if (len(label2.label) == 0):
            return label1

        l1 = label1.label
        l2 = label2.label
        i1, i2 = 0, 0
        res_li = []
        while (i1 < len(l1) and i2 < len(l2)):
            if (l1[i1][0] <= l2[i2][0]):
                res_li.append(l1[i1])
                i1 += 1
            else:
                res_li.append(l2[i2])
                i2 += 1
        while (i1 < len(l1)):
            res_li.append(l1[i1])
            i1 += 1
        while (i2 < len(l2)):
            res_li.append(l2[i2])
            i2 += 1
        return DAGNodeLabel(tuple(res_li))

class DAG:
    """
    DAG generation class

    nodes: set of DAGNodeLabels representing the labels of each node
    edges: dictionary mapping from (DAGNodeLabel1, DAGNodeLabel2) to a set of substring expressions
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
                    (serves as id for DAG node labels)
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
        # create len(output_str) + 1 number of nodes and a start node with label 0
        # since nodes are the spaces between letters
        nodes_li = []
        for i in range(1, len(output_str) + 2):
            nodes_li.append(DAGNodeLabel( ((example_ind ,i),) ))
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
                common = set()
                # for correctness, must attempt to intersect every substr expr with every other
                for substr_expr1 in self.edges[s_edge_key]:
                    for substr_expr2 in other.edges[o_edge_key]:
                        intersection = SubstrExprVSA.intersect(substr_expr1, substr_expr2) 
                        if intersection:
                            common.add(intersection)

                if common:
                    n1 = DAGNodeLabel.join(o_edge_key[0], s_edge_key[0])
                    n2 = DAGNodeLabel.join(o_edge_key[1], s_edge_key[1])
                    new_nodes.add(n1)
                    new_nodes.add(n2)
                    new_edges[(n1, n2)] = common
        self.nodes = new_nodes
        self.edges = new_edges
