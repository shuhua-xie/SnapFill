import InputDataGraph as IDG

class DAG:
    """
    DAG generation class

    nodes: set of tuples representing the labels of each node
    edges: dictionary mapping from (node1, node2) to a set of substring expressions
                where each substring expression is (v_l, v_r, constant string)
                v_l, v_r = independent sets of position expressions
    """

    def __init__(self, input_str, output_str, input_graph, prev_DAG = None):
        """
        create a DAG for each input-output example and intersect with the DAG of all previous examples
        input_str: input example as string
        output_str: corresponding output example as substring
        input_graph: InputDataGraph generated from the whole dataset
        prev_DAG: intersection of the DAGs of all previous examples, defaults to None
        """

        self.nodes = set()
        self.edges = dict()
        self.generate_DAG(input_str, output_str, input_graph)
        if prev_DAG:
            self.intersect(prev_DAG)

    def generate_DAG(self, input_str, output_str, input_graph):
        """
        first function called when generating a DAG, creates the graph for a single input-output example
        assumes:  nodes and edges are empty, input_str is non-empty
        returns:  nothing
        modifies: fills in nodes and edges as specified
        """
        # get start index and end index of output string in input string
        match = re.finditer(output_str, input_str)
        start_index = match.start()
        end_index = match.end()

        # create len(output_str) number of nodes and a start node with label 0
        for i in range(0, len(out_str)):
            self.nodes.add((i,))

        # Iterate over all substrings output_str[i..j] of the output string and add an edge (i,j) between the labels i and j
        for i in range(start_index, end_index - 1, 1):
            for j in range(i + 1, end_index, 1):
                label = ((i,), (j,))
                self.edges.setdefault(label, set())
                substr = in_str[i:j]

                # create two independent sets of position expressions v_l and v_r
                # a set of position expression consists of a set of IDG nodes and a constant position
                v_l, v_r = set()
                for v in input_graph.nodes:
                    if i in v:
                        v_l.add(v)
                    if j in v:
                        v_r.add(v)

                # add constant position to v_l and v_r
                v_l.add(i)
                v_r.add(j)

                # add independent sets of IDG nodes and constant string for given substring
                self.edges[label].add(v_l, v_r, substr)

    def intersect(self,other):
        new_nodes = set()
        new_edges = dict()
        for s_edge_key in self.edges.keys():
            for o_edge_key in other.edges.keys():

                # find common nodes of both independent sets respectively
                common = set.intersection(self.edges[s_edge_key][0], other.edges[o_edge_key][0])
                common_vr = set.intersection(self.edges[s_edge_key][1], other.edges[o_edge_key][1])
                if common_vr:
                    common.add(common_vr)
                common_str = set.intersection(self.edges[s_edge_key][2], other.edges[o_edge_key][2])
                if common_str:
                    common.add(common_str)
                if common:
                    n1 = o_edge_key[0] + s_edge_key[0]
                    n2 = o_edge_key[1] + s_edge_key[1]
                    new_nodes.add(n1)
                    new_nodes.add(n2)
                    new_edges[(n1, n2)] = common
        self.nodes = new_nodes
        self.edges = new_edges
