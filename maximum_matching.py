# A graph contains an augmenting path if an only if the matching is not maximum

import networkx as nx
import matplotlib.pyplot as plt
import random
random.seed(42)

class Tree:
    def __init__(self, value, children, parent):
        self.value = value
        self.children = children
        self.parent = parent
    def __repr__(self):
        return "Tree Object: (Value: {}, Children: {})".format(self.value, self.children)
    def height(self):
        if self.parent == None:
            return 0
        else:
            return self.parent.height() + 1
    def root(self):
        if self.parent == None:
            return self
        else:
            return self.parent.root()
    def node_list(self):
        node_list = [self]
        for child in self.children:
            node_list = node_list + child.node_list()
        return node_list
    def add_child(self, value):
        tree = Tree(value, [], self)
        self.children.append(tree)
        return tree

def get_node_tree(forest, node_val):
    for tree in forest:
        for node in tree.node_list():
            if node.value == node_val:
                return node
    return False


def find_unmarked_node_with_even_distance(G, forest, exposed_nodes):
    for tree in forest:
        for node in tree.node_list():
            if node.value not in G.graph['marked_nodes'] and node.height() % 2 == 0 and node.value in exposed_nodes:
                return node
    return False

def find_unmarked_incident_edge(G, starting_node):
    for edge in G.edges(starting_node):
        if edge not in G.graph['marked_edges']:
            return edge
    return False

def find_node_in_tree(tree, node):
    traversing = [tree]
    while traversing:
        t_node = traversing[0]
        if t_node.value == node:
            return t_node
        else:
            traversing = (traversing + t_node.children)[1:]
    return False

def path_to_parent(origin):
    path = []
    current = origin
    while current.parent:
        path.append((current.value, current.parent.value))
        current = current.parent
    return path

def get_blossom_path(v, w, blossom_edges):
    if v == w:
        return []
    path = []
    seen = False
    v_is_first_checker = 1
    for edge in ((blossom_edges + blossom_edges)):
        if v == edge[0]:
            seen = True
            v_is_first = 0
        if seen:
            path.append(edge)
        if edge[1] == w:
            if len(path) % 2 != 1:
                return path
            break
    
    path = []
    seen = False
    for edge in list(map(lambda x: tuple(reversed(x)), (blossom_edges + blossom_edges)))[::-1]:
        if v == edge[0]:
            seen = True
            v_is_first = 0
        if seen:
            path.append(edge)
        if edge[1] == w:
            if len(path) % 2 != 1:
                return path
            break
    
    print("Code should not reach here")
    quit()

def is_same_edge(edge1, edge2):
    if edge1 == edge2:
        return True
    if edge1[0] == edge2[1] and edge1[1] == edge2[0]:
        return True
    return False

def get_edges_in_node_order(path):
    new_path = []
    i = 0
    while len(new_path) < len(path):
        if i == 0:
            if path[i][0] in path[1]:
                new_path.append((path[i][1], path[i][0]))
            elif path[i][1] in path[1]:
                new_path.append((path[i][0], path[i][1]))
            else:
                print('This should not happen; case 1')
                exit()
        else:
            if path[i][0] in new_path[i-1]:
                new_path.append((path[i][0], path[i][1]))
            elif path[i][1] in new_path[i-1]:
                new_path.append((path[i][1], path[i][0]))
            else:
                print('This should not happen; case 2')
                exit()
        i += 1
    return new_path


def find_augmenting_path(G):
    # print('---------------edges_in_matching*')
    # print(G.graph['matching'].edges())
    # print('---------------edges_in_matching*')
    forest = []
    G.graph['marked_nodes'] = []
    G.graph['marked_edges'] = []
    for edge in G.graph['matching'].edges:
        G.graph['marked_edges'].append(edge)
    exposed_nodes = []
    for node in list(set(list(G.nodes)) - set(list(G.graph['matching'].nodes))):
        exposed_nodes.append(node)
        forest.append(Tree(node, [], None))
    while len(exposed_nodes) != 0:
        starting_node_val = exposed_nodes.pop(0)
        starting_node = get_node_tree(forest, starting_node_val)
        if starting_node.value in G.graph['marked_nodes']:
            continue
        if not starting_node:
            break
        while True:
            e = find_unmarked_incident_edge(G, starting_node.value)
            if not e:
                break
            w = e[0] if e[1] == starting_node.value else e[1]
            for tree in forest:
                w_sub_tree = find_node_in_tree(tree, w)
                if w_sub_tree:
                    break
            if not w_sub_tree:
                w_sub_tree = starting_node.add_child(w)
                for _e_ in G.graph['matching'].edges:
                    if _e_[0] == w:
                        x = _e_[1]
                        x_sub_tree = w_sub_tree.add_child(x)
                        exposed_nodes.append(x)
                    elif _e_[1] == w:
                        x = _e_[0]
                        x_sub_tree = w_sub_tree.add_child(x)
                        exposed_nodes.append(x)
            else:
                # print('reached1')
                #print(w_sub_tree.height())
                if w_sub_tree.height() % 2 != 0:
                    pass
                else:
                    if starting_node.root() != w_sub_tree.root():
                        # print('hereeeee')
                        # print(starting_node)
                        # print(w_sub_tree)
                        path = path_to_parent(starting_node)[::-1]
                        # print(path)
                        path.append(e)
                        path = path + path_to_parent(w_sub_tree)
                        return path
                    else:
                        #print('Blossom code reached...')
                        vpath = path_to_parent(starting_node)[::-1]
                        wpath = path_to_parent(w_sub_tree)[::-1]
                        while vpath and wpath and is_same_edge(vpath[0], wpath[0]):
                            vpath.pop(0)
                            wpath.pop(0)
                        blossom_edges = vpath + [e] + wpath[::-1]
                        nodes_in_path = []
                        for edge in blossom_edges:
                            for node in edge:
                               nodes_in_path.append(node) 
                        unique_nodes_in_path = [nodes_in_path[0]] + list(set(nodes_in_path) - {nodes_in_path[0]})
                        contracted_graph = nx.Graph()
                        contracted_graph.graph['matching'] = nx.Graph()
                        for edge in G.edges:
                            new_edge = (
                                unique_nodes_in_path[0] if edge[0] in unique_nodes_in_path else edge[0],
                                unique_nodes_in_path[0] if edge[1] in unique_nodes_in_path else edge[1]
                            )
                            if not contracted_graph.has_edge(*new_edge) and new_edge[0] != new_edge[1]:
                                #print(new_edge)
                                contracted_graph.add_edge(*new_edge)
                        for edge in G.graph['matching'].edges:
                            if edge[0] not in unique_nodes_in_path[1:] and edge[1] not in unique_nodes_in_path[1:]:
                                contracted_graph.graph['matching'].add_edge(*edge)
                        path = find_augmenting_path(contracted_graph)
                        if path == []:
                            # print('return 1')
                            return []
                        connected_edges = []
                        does_path_interact_with_blossom = False
                        for edge in path:
                            if edge[0] in unique_nodes_in_path or edge[1] in unique_nodes_in_path:
                                # print(edge)
                                connected_edges.append(edge)
                                does_path_interact_with_blossom = True
                        if not does_path_interact_with_blossom:
                            # print('return 2')
                            return path
                        edge_entering = False
                        edge_leaving = False
                        for edge in connected_edges:
                            if edge[0] == unique_nodes_in_path[0]:
                                node = edge[1]
                            else:
                                node = edge[0]
                            potential_edges = []
                            for _edge in G.edges:
                                if (_edge[0] == node and _edge[1] in unique_nodes_in_path) or (_edge[1] == node and _edge[0] in unique_nodes_in_path):
                                    # print(edge)
                                    potential_edges.append(_edge)
                            for __edge in potential_edges:
                                if (__edge[0] == unique_nodes_in_path[0]) or (__edge[1] == unique_nodes_in_path[0]):
                                    edge_entering = __edge
                                    # print(edge_entering)
                                    break
                            if not edge_entering:
                                edge_leaving = (
                                    potential_edges[0][0] if potential_edges[0][0] not in unique_nodes_in_path else potential_edges[0][1],
                                    potential_edges[0][0] if potential_edges[0][0] in unique_nodes_in_path else potential_edges[0][1]
                                )
                                # print('--near_end')
                                # print(connected_edges)
                                # print(path)
                                # print(edge)
                                ind = path.index(edge)
                        if not edge_leaving:
                            # print('return 3')
                            return path

                        path_of_blossom = get_blossom_path(unique_nodes_in_path[0], edge_leaving[1], blossom_edges)
                        
                        if ind >= 1 and unique_nodes_in_path[0] in path[ind]:
                            path_of_blossom = path_of_blossom[::-1]
                        # print('return 4')
                        return path[:ind] + path_of_blossom + [edge_leaving] + path[(ind+1):]
                    
            # mark edge e
            G.graph['marked_edges'].append(e)
        G.graph['marked_nodes'].append(starting_node.value)
    return [] # intention is to return an empty path here

    

def find_maximum_matching(G):
    # print('------------beginning func call')
    path = find_augmenting_path(G)
    if path:
        # print('----------path1')
        # print(path)
        # print('----------path2')
        for edge in path:
            if G.graph['matching'].has_edge(*edge):
                G.graph['matching'].remove_edge(*edge)
            else:
                G.graph['matching'].add_edge(*edge)
        # print('----------matching1')        
        # print(G.graph['matching'].edges)
        # print('----------matching2')
        return find_maximum_matching(G)
    else:
        return G

def find_maximum_matching_wrapper(G):
    G.graph['matching'] = nx.Graph()
    G.graph['marked_nodes'] = []
    G.graph['marked_edges'] = []
    G = find_maximum_matching(G)
    return G