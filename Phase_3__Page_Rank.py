import json


class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

    def __eq__(self, other):
        assert isinstance(other, Edge)
        return self.from_node == other.from_node and self.to_node == other.to_node

    def __repr__(self):
        return "From Node " + str(self.from_node) + '\nTo Node ' + str(self.to_node) + '\n'


class Node:
    def __init__(self, link):
        self.link = link
        self.out_edges = []
        self.in_edges = []
        self.pr = 0.0
        self.new_pr = 0.0

    def __eq__(self, other):
        assert isinstance(other, Node)
        return self.link == other.link

    def __lt__(self, other):
        assert isinstance(other, Node)
        return self.link < other.link

    def __repr__(self):
        return "Link: " + str(self.link) + " / PR: " + str(self.pr)


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, link):
        if self.get_node(link) is None:
            self.nodes.append(Node(link))

    def add_edge(self, from_link, to_link):
        from_node = self.get_node(from_link)
        to_node = self.get_node(to_link)
        edge = Edge(from_node, to_node)
        if self.get_edge(edge) is None:
            self.edges.append(edge)
            from_node.out_edges.append(edge)
            to_node.in_edges.append(edge)

    def get_node(self, lnk):
        for node in self.nodes:
            if node.link == lnk:
                return node
        return None

    def get_edge(self, edge):
        for eg in self.edges:
            if eg == edge:
                return eg
        return None

    def init_rank(self):
        pr = 1.0 / len(self.nodes)
        for node in self.nodes:
            node.pr = pr

    def update_rank(self):
        for node in self.nodes:
            from_nodes = []
            for edge in node.in_edges:
                from_nodes.append(edge.from_node)
            pr = 0.0
            for nd in from_nodes:
                pr += nd.pr / len(nd.out_edges)
            node.new_pr = pr
        for node in self.nodes:
            node.pr = node.new_pr

    def get_sorted_nodes(self):
        nodes = self.nodes.copy()
        prs = []
        for node in nodes:
            prs.append(node.pr)
        zipped_pairs = zip(prs, nodes)
        sorted_nodes = [x for _, x in sorted(zipped_pairs)]
        sorted_nodes.reverse()
        prs.sort(reverse=True)

        return sorted_nodes, prs


with open('Phase3_PageRank_in.json') as json_file:
    data = json.load(json_file)

gr = Graph()

for page in data:
    link = page['link']
    refs = page['refs']

    gr.add_node(link)
    for ref in refs:
        gr.add_node(ref)
        gr.add_edge(link, ref)

# For Test
# gr.add_node('a')
# gr.add_node('b')
# gr.add_node('c')
# gr.add_node('d')
#
# gr.add_edge('a', 'b')
# gr.add_edge('a', 'c')
# gr.add_edge('b', 'd')
# gr.add_edge('c', 'a')
# gr.add_edge('c', 'b')
# gr.add_edge('c', 'd')
# gr.add_edge('d', 'c')

gr.init_rank()
for i in range(10):
    gr.update_rank()

nodes, prs = gr.get_sorted_nodes()

# for node in gr.nodes:
#     print(node)
