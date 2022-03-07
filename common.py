"""
common.py
used for both IDG and DAG
"""
import bisect

def topsort(nodes, edge_keys):
    """
    input: input data graph
    output: list of topologically sorted nodes
    """
    # dict for indegree of each node in IDG
    indeg = dict()
    for n in nodes:
        indeg[n] = 0
    for edge_key in edge_keys:
        indeg[edge_key[1]] += 1

    # create a queue and enqueue all vertices with indegree 0
    queue = [node for node in indeg.keys() if indeg[node] == 0]

    # list to store the topological ordering of the vertices
    topsort = []
    while queue:
        # Taking front node of the queue and adding it into the topsort list.
        node = queue.pop(0)
        topsort.append(node)
        # Iterate through all the neighbouring nodes of dequeued node and decrease their in-degree by 1
        for edge_key in edge_keys:
            if edge_key[0] == node:
                indeg[edge_key[1]] -= 1
                # If the indegree of the neighbour becomes 0 add it to the queue.
                if indeg[edge_key[1]] == 0:
                    queue.append(edge_key[1])
    return topsort


class NodeLabel:
    """
    represents the label of a DAG node
    is a tuple of tuples, the outer one maintains a sorted property
        inner ones are pairs, representing (id, index)

    label: tuple of tuples

    supported operations: 
    NodeLabel.join(), joins two node labels into 1, assumes the two label's ids are disjoint
    self.indexof(), given id, returns the index or None
    """
    def __init__(self, label):
        self.label = label

    def __eq__(self, other):
        if isinstance(other, NodeLabel):
            return self.label == other.label
        return False

    def __lt__(self, other):
        return self.label.__lt__(other.label)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "label<<" + self.label.__str__() + ">>"

    def __hash__(self):
        return hash(self.label)

    def __getitem__(self, ind):
        """
        input: an id (int)
        output: corresponding id's index (or None if it isn't present)
        """
        ids, inds = tuple(zip(*self.label))
        expect_i = bisect.bisect_left(ids, ind)
        if (expect_i == len(ids) or ids[expect_i] != ind):
            return None
        return inds[expect_i]

    def ids(self):
        """
        returns: tuple of ids represented in this DAG label
        note: it's in sorted order
        """
        ids, inds = tuple(zip(*self.label))
        return ids

    def inds(self):
        """
        returns: tuple of ids represented in this DAG label
        note: it's in sorted order
        """
        ids, inds = tuple(zip(*self.label))
        return inds

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
        return NodeLabel(tuple(res_li))

