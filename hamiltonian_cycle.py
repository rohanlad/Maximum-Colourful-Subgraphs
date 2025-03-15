import networkx as nx
import copy
import random
random.seed(42)
# A Hamiltonian cycle is a cycle through a graph that visits each node exactly once.
# We can compute the length of a longest cycle in a graph
# If the number of nodes in this longest cycle = the number of nodes in the graph, the cycle is Hamiltonian

def hamiltonicity_of_bipartite(G_star, I, dom_vertices_subset, degree_list_iso, degree_list_dom, r):
    ham = True
    # print('-------degreelists')
    # print(degree_list_dom)
    # print(degree_list_iso)
    for q in range(0, r):
        for j in range(1, q+1):
            if degree_list_iso[j-1] < (j + 1):
                ham = False
        for j in range(1, (r-q)):
            if degree_list_dom[j-1] < (j + 1):
                ham = False
    if ham == False:
        return [[]]
    else:
        if (r % 2) == 0: # if r is even
            nodes = set((I[0], dom_vertices_subset[r-1])) # used to keep track of all the nodes in the constructed cycle
            cycle = [(I[0], dom_vertices_subset[r-1])] # (x1, yr)
            # print('--------------infoavailable')
            # print(I)
            # print(dom_vertices_subset)
            # print(r)
            # print('--------------infoavailable')
            ycount = 1
            xcount = 1
            # print('-----ckpt0')
            # print(cycle)
            while (r-ycount) >= 1:
                u = dom_vertices_subset[r-ycount]
                v = I[xcount]
                cycle.append((u,v))
                nodes.update([u, v])
                if xcount != (r-1):   
                    cycle.append((v, dom_vertices_subset[r-ycount-2]))
                    nodes.update([dom_vertices_subset[r-ycount-2]])
                ycount = ycount + 2
                xcount = xcount + 2
            cycle.append((I[r-1], dom_vertices_subset[0])) # (xr, y1)
            # print('--------ckpt1')
            # print(cycle)
            nodes.update([I[r-1], dom_vertices_subset[0]])
            ycount_ = 0
            xcount_ = 2
            while ycount_ <= (r-2):
                u = dom_vertices_subset[ycount_]
                v = I[r-xcount_]
                cycle.append((u,v))
                nodes.update([u, v])
                if (r-xcount_) != 0:
                    cycle.append((v, dom_vertices_subset[ycount_+2]))
                    nodes.update([dom_vertices_subset[ycount_+2]])
                ycount_ = ycount_ + 2
                xcount_ = xcount_ + 2
            return [cycle, nodes]
        else: # if r is odd
            cycle = [(I[0], dom_vertices_subset[r-1])]
            nodes = set((I[0], dom_vertices_subset[r-1]))
            ycount = 1
            xcount = 1
            # print('-----------infooddr')
            # print(I)
            # print(dom_vertices_subset)
            # print(r)
            # print('-----------infooddr')
            while xcount <= (r-2):
                u = dom_vertices_subset[r-ycount]
                v = I[xcount]
                cycle.append((u,v))
                nodes.update([u, v])
                ycount = ycount + 2
                xcount = xcount + 2
            cycle.append((I[r-2], dom_vertices_subset[0])) # (xr-1, y1)
            cycle.append((dom_vertices_subset[0], I[r-1])) # (y1, xr)
            cycle.append((I[r-1], dom_vertices_subset[1])) # (xr, y2)
            nodes.update([I[r-2], dom_vertices_subset[0], I[r-1], dom_vertices_subset[1]])
            ycount_ = 1
            xcount_ = 3
            while ycount_ <= (r-2):
                u = dom_vertices_subset[ycount_]
                v = I[r-xcount_]
                cycle.append((u,v))
                nodes.update([u, v])
                ycount_ = ycount_ + 2
                xcount_ = xcount_ + 2
            return [cycle, nodes]


# Function takes in a threshold graph as input, the candidate nodes for the Hamiltonian Cycle, 
# and metadata that tells you which nodes are isolating and which are dominating, and 
# returns a Hamiltonian cycle.
def is_hamiltonian(G, is_dominating_vertex__):
    first_node = min(list(G.nodes()))
    is_dominating_vertex = copy.deepcopy(is_dominating_vertex__)
    if is_dominating_vertex[first_node]:
        is_dominating_vertex[first_node] = False
    # print('------------is_hamiltonian_input_graph')
    # print(G.nodes())
    # print(G.edges())
    # print(is_dominating_vertex)
    # print('------------is_hamiltonian_input_graph')
    I = [] # the isolated vertices
    K = [] # the dominating vertices
    for v in list(G.nodes()):
        if is_dominating_vertex[v]:
            K.append(v)
        else:
            I.append(v)
    r = len(I)
    s = len(K) 
    K = sorted(K)
    I = sorted(I, reverse=True)
    if r == 0:
        if s < 3:
            return []
        else:
            # return y1, y2, ... ys, y1
            cycle = []
            for i in range(0, len(list(G.nodes()))-1):
                # print((list(G.nodes())[i], list(G.nodes())[i+1]))
                cycle.append((list(G.nodes())[i], list(G.nodes())[i+1]))
            cycle.append((list(G.nodes())[-1], list(G.nodes())[0]))
            return cycle
    elif r == 1:
        if G.degree[I[0]] < 2:
            return []
        else:
            x1_neighbours = sorted(list(G.neighbors(I[0])))
            y_k = x1_neighbours[0]
            y_l = x1_neighbours[1]
            cycle = [(I[0], y_k)]
            dominating_vertexes_to_add = K
            dominating_vertexes_to_add.remove(y_k)
            dominating_vertexes_to_add.remove(y_l)
            if len(dominating_vertexes_to_add) > 0:
                while True:
                    cycle.append((cycle[-1][1], dominating_vertexes_to_add.pop()))
                    if len(dominating_vertexes_to_add) == 0:
                        break
            cycle = cycle + [(cycle[-1][1], y_l), (y_l, I[0])]
            return cycle
    else: # i.e r >= 2
        if r > s:
            return []
        else: # i.e 2 <= r <= s
            dom_vertices_subset = K[(s-r):]
            # print('----subset')
            # print(dom_vertices_subset)
            degree_list_dom = []
            degree_list_iso = []
            for dominating_vertex in dom_vertices_subset:
                degree_list_dom.append(G.degree[dominating_vertex])
            for isolated_vertex in I:
                degree_list_iso.append(G.degree[isolated_vertex])
            new_vertex_list = dom_vertices_subset + I
            G_star = G.subgraph(new_vertex_list).copy()
            for edge in G_star.edges:
                if edge[0] in K and edge[1] in K:
                    G_star.remove_edge(*edge)
            cycle_from_bipartite = hamiltonicity_of_bipartite(G_star, I, dom_vertices_subset, degree_list_iso, degree_list_dom, r)
            # print('--------outputfrombipartite')
            # print(cycle_from_bipartite[0])
            # print('--------outputfrombipartite')
            if cycle_from_bipartite[0] == []:
                return []
            else:
                if (s-r) == 0:
                    return cycle_from_bipartite[0]
                else:
                    # print('--------neighbours')
                    # print(list(G.neighbors(K[s-r-1])))
                    for candidate_neighbour in list(G.neighbors(K[s-r-1])):
                        if candidate_neighbour in cycle_from_bipartite[1] and candidate_neighbour in I:
                            aj = candidate_neighbour
                            break
                    for i in range(0, len(cycle_from_bipartite[0])):
                        if cycle_from_bipartite[0][i][0] == aj:
                            aj_index = i 
                            break
                    cycle = cycle_from_bipartite[0][:aj_index]
                    cycle.append((aj, K[s-r-1]))
                    count = s-r-1
                    while count > 0:
                        cycle.append((K[count], K[count-1]))
                        count = count - 1
                    cycle.append((K[0], cycle_from_bipartite[0][aj_index][1]))
                    cycle.extend(cycle_from_bipartite[0][(aj_index+1):])
                    return cycle