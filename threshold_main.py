
import networkx as nx
from maximum_matching import find_maximum_matching_wrapper
from tropical_matching import find_max_colourful_matching
from hamiltonian_cycle import is_hamiltonian
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from generate_graph import generate_graph, generate_graph_2
import numpy as np
import random
from time import process_time
import matplotlib.pyplot as plt
from random import randrange
import math

random.seed(42)


def algorithm1(G):
    t1_start = process_time() 

    # Compute the maximum matching of this graph (which is subsequently stored inside the graph variable)
    t1_maximum_matching_start = process_time() 
    G = find_maximum_matching_wrapper(G)
    # print('-------matching')
    # print(G.graph['matching'].edges())
    t1_maximum_matching_stop = process_time()
    #print("Elapsed time during the maximum matching calculation in seconds:",t1_maximum_matching_stop-t1_maximum_matching_start) 
    # print('-----------max-matching')
    # print(G.graph['matching'].edges())
    # print('-----------max-matching')


    
    # Compute the number of colours of a maximum colourful matching of this graph
    compute_colourful_matching = find_max_colourful_matching(G)
    M = compute_colourful_matching[0]
    # print('----max_colourful_matching')
    # print(M.edges())
    # print('----max_colourful_matching')
    num_colours = compute_colourful_matching[1]
    # print('Cm value: ' + str(num_colours)) # this is our Cm value

    # ********************
    # Case 1.1
    # ********************

    # X ~ the set of dominating vertices
    X = set()
    # Y ~ the set of isolated vertices
    Y = set()
    for i in range(0, len(G.graph['dominating_vertices'])):
        if G.graph['dominating_vertices'][i] == True:
            X.add(i)
        else:
            Y.add(i)
    # print('X: ' + str(X))
    # print('Y: ' + str(Y))
    Y_ordered = sorted(list(Y))

    # C2 ~ the set of colours in X
    C2 = set()
    # CY ~ the set of colours in Y
    CY = set()
    for node in X:
        C2.add(G.graph['colour_map'][node])
    for node in Y:
        CY.add(G.graph['colour_map'][node])
    # C1 ~ the set of colours in Y but not in X
    C1 = CY - C2
    # print('C1: ' + str(C1))
    # print('C2: ' + str(C2))

    # For each colour in C1, we establish the first node in Y with this colour
    # Repeat for all colours in C1 and add all outcome nodes to a list vertex_min_list
    vertex_min_list = set()
    for colour in C1:
        for node in Y_ordered:
            if G.graph['colour_map'][node] == colour:
                vertex_min_list.add(node)
                break
    # print('vertex_min_list: ' + str(vertex_min_list))

    # candidate_vertices = V(X) U vertex_min_list
    candidate_vertices_case11 = X.union(vertex_min_list)
    # print('candidate_vertices for case 1.1: ' + str(candidate_vertices_case11))

    candidate_subgraph = G.subgraph(candidate_vertices_case11).copy()
    # print('case1.1 checking for hamiltonian ')
    ham_cycle = is_hamiltonian(candidate_subgraph, G.graph['dominating_vertices'])
    if ham_cycle != []:
        # print('---outputfromcase1.1')
        ham_cycle_g = nx.Graph()
        ham_cycle_g.add_edges_from(ham_cycle)
        t1_stop = process_time()
        print("Elapsed time during the whole program in seconds:",t1_stop-t1_start) 
        return [ham_cycle_g, t1_maximum_matching_stop-t1_maximum_matching_start, t1_stop-t1_start, t1_stop-t1_maximum_matching_stop]

    else:
    # ********************
    # Case 1.2
    # ********************

        for node in Y:
            # Xplus ~ the set of dominating vertices added to the graph after node
            Xplus = set()
            for dominating_vertex in X:
                if dominating_vertex > node:
                    Xplus.add(dominating_vertex)
            # Xplus_colours ~ the set of colours amongst the vertices in Xplus
            Xplus_colours = set()
            for n in Xplus:
                Xplus_colours.add(G.graph['colour_map'][n])
            # Run check to detect if this node is the unique vertex
            if ((len(Xplus) + len(Xplus_colours)) != (num_colours + 1)):
                continue
            # print('------------foundv*')
            # print(node)
            # print('------------foundv*')
            # colour_list_12 ~ the set of colours in Y that aren't in Xplus_colours
            colour_list_12 = CY - Xplus_colours
            # For each colour in colour_list_12, we establish the first node in Y with this colour
            # Repeat for all colours in colour_list_12 and add all outcome nodes to a list vertex_min_list_dash
            vertex_min_list_dash = set()
            for colour in colour_list_12:
                for nd in Y_ordered:
                    if G.graph['colour_map'][nd] == colour:
                        vertex_min_list_dash.add(nd)
                        break
            # print('vertex_min_list_dash: ' + str(vertex_min_list_dash))
            # candidate_vertices_case12 = V(Xplus(v)) U vertex_min_list_dash
            candidate_vertices_case12 = Xplus.union(vertex_min_list_dash)
            # print('candidate_vertices for case 1.2: ' + str(candidate_vertices_case12))
            candidate_subgraph = G.subgraph(candidate_vertices_case12).copy()
            ham_cycle = is_hamiltonian(candidate_subgraph, G.graph['dominating_vertices'])
            if ham_cycle != []:
                ham_cycle_g = nx.Graph()
                ham_cycle_g.add_edges_from(ham_cycle)
                t1_stop = process_time()
                print("Elapsed time during the whole program in seconds:",t1_stop-t1_start) 
                return [ham_cycle_g, t1_maximum_matching_stop-t1_maximum_matching_start, t1_stop-t1_start, t1_stop-t1_maximum_matching_stop]
            else:
                break
    


    # ********************
    # Case 2.1
    # ********************
    for node in X:
        # colour_list_21 ~ C1 union the colour of the node
        colour_list_21 = C1.union(set([G.graph['colour_map'][node]]))
        vertex_min_list_dash_2 = []
        # l ~ Cm - |C(X)| + 1
        l = num_colours - len(C2) + 1
        for colour in colour_list_21:
            for nd in Y_ordered:
                if G.graph['colour_map'][nd] == colour:
                    vertex_min_list_dash_2.append(nd)
                    break
        vertex_min_list_dash_2 = sorted(vertex_min_list_dash_2)[:l]
        candidate_vertices_case21 = (X - set([node])).union(set(vertex_min_list_dash_2))
        # print('-------candidateverticesforcase2.1')
        # print(candidate_vertices_case21)
        # print('-------candidateverticesforcase2.1')
        candidate_subgraph = G.subgraph(candidate_vertices_case21).copy()
        ham_cycle = is_hamiltonian(candidate_subgraph, G.graph['dominating_vertices'])
        if ham_cycle != []:
            # print('output is from case2.1')
            ham_cycle_g = nx.Graph()
            ham_cycle_g.add_edges_from(ham_cycle)
            t1_stop = process_time()
            print("Elapsed time during the whole program in seconds:",t1_stop-t1_start) 
            return [ham_cycle_g, t1_maximum_matching_stop-t1_maximum_matching_start, t1_stop-t1_start, t1_stop-t1_maximum_matching_stop]

    # ********************
    # Case 2.2
    # ********************

    # For each colour in C2, we establish the last node in X with this colour
    # Repeat for all colours in C2 and add all outcome nodes to a list vertex_max_list
    vertex_max_list = set()
    for colour in C2:
        for node in sorted(list(X), reverse=True):
            if G.graph['colour_map'][node] == colour:
                vertex_max_list.add(node)
                break
    X_minus_max_list = X - vertex_max_list 
    for t in range(0, len(X_minus_max_list)+1):
        # X_t ~ the t last vertices in X_minus_max_list
        X_t = set(sorted(list(X_minus_max_list))[-t:])
        # l = Cm - |C(X)|
        vertex_min_list_2 = []
        l = num_colours - len(C2)
        for colour in C1:
            for node in Y_ordered:
                if G.graph['colour_map'][node] == colour:
                    vertex_min_list_2.append(node)
                    break
        vertex_min_list_2 = sorted(vertex_min_list_2)[:l]
        candidate_vertices_case22 = X_t.union(vertex_max_list).union(set(vertex_min_list_2))
        # print('Candidate vertices for case 2.2: ' + str(candidate_vertices_case22))
        candidate_subgraph = G.subgraph(candidate_vertices_case22).copy()
        # print('checking ham for case2.2')
        ham_cycle = is_hamiltonian(candidate_subgraph, G.graph['dominating_vertices'])
        if ham_cycle != []:
            # print('output is from case2.2')
            ham_cycle_g = nx.Graph()
            ham_cycle_g.add_edges_from(ham_cycle)
            t1_stop = process_time()
            print("Elapsed time during the whole program in seconds:",t1_stop-t1_start) 
            return [ham_cycle_g, t1_maximum_matching_stop-t1_maximum_matching_start, t1_stop-t1_start, t1_stop-t1_maximum_matching_stop]


    # ********************
    # Case 3
    # ********************

    # choose one dominating vertex from each edge of M: denote those vertices by x1, x2, . . . , x|M|, such that xj was added earlier than xj+1, for 1 ≤ j ≤ |M|−1.
    dominating_vertex_choices = []
    for edge in M.edges():
        if G.graph['dominating_vertices'][edge[0]] and edge[0] not in dominating_vertex_choices:
            dominating_vertex_choices.append(edge[0])
        elif G.graph['dominating_vertices'][edge[1]] and edge[1] not in dominating_vertex_choices:
            dominating_vertex_choices.append(edge[1])
    dominating_vertex_choices = sorted(dominating_vertex_choices)
    # print('dominating-vertex-choices')
    # print(dominating_vertex_choices)
    # print('dominating-vertex-choices')
    dominating_vertex_choices_neighbours = []
    for vertex in dominating_vertex_choices:
        dominating_vertex_choices_neighbours.append(list(M.neighbors(vertex))[0])
    cycle = nx.Graph()
    for i in range(0, len(M.edges())-1):
        cycle.add_edge(dominating_vertex_choices[i], dominating_vertex_choices_neighbours[i])
        cycle.add_edge(dominating_vertex_choices_neighbours[i], dominating_vertex_choices[i+1])
        # print('---------case3cycle-sofar')
        # print(cycle.edges())
        # print('---------case3cycle-sofar')
    cycle.add_edge(dominating_vertex_choices[len(M.edges())-1], dominating_vertex_choices[0])
    # print('Cycle constructed via case 3')
    t1_stop = process_time()
    print("Elapsed time during the whole program in seconds:",t1_stop-t1_start) 
    return [cycle, t1_maximum_matching_stop-t1_maximum_matching_start, t1_stop-t1_start, t1_stop-t1_maximum_matching_stop]


#*******************************************************************************
x_axis = []
y_axis_alg_excluding_matching = []
y_axis_entire_program = []
y_axis_entire_program_square_rooted = []
y_axis_proposed_big_o = []


'''
# FIXING NUMBER OF EDGES AND COLOURS, VARYING NUMBER OF NODES
def varying_nodes():
    num_colours = 3
    fixed_num_edges = 100
    count_ = 0
    min_node_count = 0
    while count_ < fixed_num_edges:
        count_ += min_node_count
        min_node_count += 1
    print('min-node-count: ' + str(min_node_count))     
    offset = 1/(fixed_num_edges-min_node_count+1)
    for u in range(min_node_count, fixed_num_edges+2):
        x_axis.append(u)
        print('u: ' + str(u))
        if offset > 0.999:
            offset = 1
        G = generate_graph(0,0,num_colours, u, fixed_num_edges, offset) 
        func_return_output = algorithm1(G)
        output = func_return_output[0]
        print('Output: ' + str(output.edges()))
        matching_time = func_return_output[1]
        entire_alg_time = func_return_output[2]
        alg_excluding_max_matching = func_return_output[3]
        y_axis_entire_program.append(entire_alg_time)
        y_axis_alg_excluding_matching.append(alg_excluding_max_matching)
        y_axis_proposed_big_o.append(max((num_colours*fixed_num_edges*u*u), (u*(u+fixed_num_edges))))
        offset += 1/(fixed_num_edges-min_node_count+2)
        # ********* VISUALISATION *********
        # for e in G.edges():
        #     G[e[0]][e[1]]['color'] = 'grey'
        # for edge in output.edges():
        #     G[edge[0]][edge[1]]['color'] = 'red'
        # # Store in a list to use for drawing
        # edge_color_list = [G[e[0]][e[1]]['color'] for e in G.edges()]
        # pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())), iterations=20)
        # nx.draw(G, node_color=G.graph['colour_map'], nodelist=sorted(list(G.nodes())), edge_color = edge_color_list, with_labels = True, pos=pos)
        # plt.show()
        # ********* VISUALISATION *********

    plt.plot(x_axis, y_axis_entire_program)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Total Program Run time')
    plt.title('Number of nodes vs total program run time')
    plt.show()

    # plt.plot(x_axis, y_axis_alg_excluding_matching)
    # plt.xlabel('Number of Nodes')
    # plt.ylabel('Program Run time (exc. max matching)')
    # plt.title('Number of nodes vs run time exc. max matching')
    # plt.show()

    plt.plot(x_axis, y_axis_proposed_big_o)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Proposed Big-O function')
    plt.title('Number of nodes vs proposed big-o function')
    plt.show()
'''

def varying_nodes_random_data_points():
    fixed_num_edges = 2000
    count_ = 0
    min_node_count = 0
    max_node_count = fixed_num_edges + 1    
    while count_ < fixed_num_edges:
        count_ += min_node_count
        min_node_count += 1
    threshold_lower = 0
    threshold_upper = 50
    rangecount = 0
    num_colours = 3 # maximum value is min_node_count
    while len(x_axis) < 2: # the number of data points you want
        if rangecount == 5:
            threshold_lower += 100
            threshold_upper += 100
            rangecount = 0
        G = generate_graph_2(num_colours, fixed_num_edges, min_node_count, max_node_count)
        if G.number_of_nodes() in x_axis: #or G.number_of_nodes() < threshold_lower or G.number_of_nodes() > threshold_upper:
            continue
        try:
            func_return_output = algorithm1(G)
        except:
            continue
        rangecount += 1
        x_axis.append(G.number_of_nodes())
        print(x_axis)
        output = func_return_output[0]
        print('Output: ' + str(output.edges()))
        matching_time = func_return_output[1]
        entire_alg_time = func_return_output[2]
        alg_excluding_max_matching = func_return_output[3]
        y_axis_entire_program.append(entire_alg_time)
        y_axis_entire_program_square_rooted.append(math.sqrt(entire_alg_time))
        y_axis_alg_excluding_matching.append(alg_excluding_max_matching)
        y_axis_proposed_big_o.append(max((num_colours*fixed_num_edges*G.number_of_nodes()*G.number_of_nodes()), (G.number_of_nodes()*(G.number_of_nodes()+fixed_num_edges))))
    
    plt.plot(x_axis, y_axis_entire_program, 'o')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Total Program Run time')
    plt.title('No. nodes vs program run time, no. colours: ' + str(num_colours) + ' , no. edges: ' + str(fixed_num_edges))
    plt.show()

    plt.plot(x_axis, y_axis_entire_program_square_rooted, 'o')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Total Program Run time, rooted')
    plt.title('No. nodes vs program run time (rooted), no. colours: ' + str(num_colours) + ' , no. edges: ' + str(fixed_num_edges))
    plt.show()

    x_axis_all = []
    y_axis_proposed_big_o_all = []
    for x in range(min_node_count, max_node_count+1):
        x_axis_all.append(x)
        y_axis_proposed_big_o_all.append(max((num_colours*fixed_num_edges*x*x), (x*(x+fixed_num_edges))))

    plt.plot(x_axis, y_axis_proposed_big_o, 'o', color='red')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Proposed Big-O function')
    plt.title('No. nodes vs proposed big-o function, no. colours: ' + str(num_colours) + ' , no. edges: ' + str(fixed_num_edges))
    plt.show()

    plt.plot(x_axis_all, y_axis_proposed_big_o_all, color='red')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Proposed Big-O function')
    plt.title('No. nodes vs proposed big-o function, no. colours: ' + str(num_colours) + ' , no. edges: ' + str(fixed_num_edges))
    plt.show()

'''
def varying_nodes_completely_random():
    num_colours = 3
    fixed_num_edges = 100
    count_ = 0
    min_node_count = 0
    while count_ < fixed_num_edges:
        count_ += min_node_count
        min_node_count += 1
    print('min-node-count: ' + str(min_node_count))     
    # for u in range(min_node_count, fixed_num_edges+2):
    for u in range(30, 70):
        x_axis.append(u)
        print('u: ' + str(u))
        G = generate_graph(0,0,num_colours, u, fixed_num_edges, 0.5) 
        func_return_output = algorithm1(G)
        output = func_return_output[0]
        print('Output: ' + str(output.edges()))
        matching_time = func_return_output[1]
        entire_alg_time = func_return_output[2]
        alg_excluding_max_matching = func_return_output[3]
        y_axis_entire_program.append(entire_alg_time)
        y_axis_alg_excluding_matching.append(alg_excluding_max_matching)
        y_axis_proposed_big_o.append(max((num_colours*fixed_num_edges*u*u), (u*(u+fixed_num_edges))))
        # ********* VISUALISATION *********
        # for e in G.edges():
        #     G[e[0]][e[1]]['color'] = 'grey'
        # for edge in output.edges():
        #     G[edge[0]][edge[1]]['color'] = 'red'
        # # Store in a list to use for drawing
        # edge_color_list = [G[e[0]][e[1]]['color'] for e in G.edges()]
        # pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())), iterations=20)
        # nx.draw(G, node_color=G.graph['colour_map'], nodelist=sorted(list(G.nodes())), edge_color = edge_color_list, with_labels = True, pos=pos)
        # plt.show()
        # ********* VISUALISATION *********

    plt.plot(x_axis, y_axis_entire_program)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Total Program Run time')
    plt.title('Number of nodes vs total program run time')
    plt.show()

    # plt.plot(x_axis, y_axis_alg_excluding_matching)
    # plt.xlabel('Number of Nodes')
    # plt.ylabel('Program Run time (exc. max matching)')
    # plt.title('Number of nodes vs run time exc. max matching')
    # plt.show()

    plt.plot(x_axis, y_axis_proposed_big_o)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Proposed Big-O function')
    plt.title('Number of nodes vs proposed big-o function')
    plt.show()
'''




# FIXING NUMBER OF NODES AND COLOURS, VARYING NUMBER OF EDGES
def varying_edges():
    fixed_num_nodes = 20
    num_colours = 3
    for c in range(1, fixed_num_nodes):
        print('--------num_dominating')
        print(c)
        print('--------num_dominating')
        count_per_dp = 0
        while count_per_dp < 40:
            G = generate_graph(c,fixed_num_nodes-c,num_colours, 0, 0)
            print('graph has been generated')
            count_per_dp += 1
            try:
                func_return_output = algorithm1(G)
            except:
                continue
            output = func_return_output[0]
            print('Output: ' + str(output.edges()))
            matching_time = func_return_output[1]
            entire_alg_time = func_return_output[2]
            # if entire_alg_time > 0.0175:
            #     continue
            if G.number_of_edges() not in x_axis:
                x_axis.append(G.number_of_edges())
            else:
                continue
            # alg_excluding_max_matching = func_return_output[3]
            y_axis_entire_program.append(entire_alg_time)
            # y_axis_alg_excluding_matching.append(alg_excluding_max_matching)
            y_axis_proposed_big_o.append(max((num_colours*c*fixed_num_nodes*fixed_num_nodes), (fixed_num_nodes*(fixed_num_nodes+c))))

    plt.plot(x_axis, y_axis_entire_program, 'o')
    plt.xlabel('Number of Edges')
    plt.ylabel('Total Program Run time')
    plt.title('No. edges vs program run time, no. colours: ' + str(num_colours) + ' , no. nodes: ' + str(fixed_num_nodes))
    plt.show()

    plt.plot(x_axis, y_axis_proposed_big_o, 'o', color='red',)
    plt.xlabel('Number of Edges')
    plt.ylabel('Proposed Big-O function')
    plt.title('No. edges vs proposed big-o function, no. colours: ' + str(num_colours) + ' , no. nodes: ' + str(fixed_num_nodes))
    plt.show()


# FIXED NUMBER OF NODES AND EDGES, VARYING NUMBER OF COLOURS
def varying_colours():
    fixed_num_nodes = 15
    proportion_dominating = 3/15
    num_dominating = math.floor(proportion_dominating*fixed_num_nodes)
    num_isolating = fixed_num_nodes - num_dominating
    G = generate_graph(num_dominating,num_isolating,0, 0, 0, 0, False)
    print('Graph has this many edges: ' + str(G.number_of_edges()))
    colour_dict = list(mcolors.CSS4_COLORS)
    # for w in range(2, fixed_num_nodes+1): if you want to use the entire node range i.e if we have 1000 nodes, test for num_colours ranging from 2 to 1000
    for w in range(2, fixed_num_nodes+1):
        print('w val: ' + str(w))
        G.graph['colour_map'] = [None] * fixed_num_nodes
        colours_to_use = colour_dict[:w]
        for colour in colours_to_use:
            while True:
                random_index = randrange(fixed_num_nodes)
                if G.graph['colour_map'][random_index] == None:
                    G.graph['colour_map'][random_index] = colour
                    break
        for j in range(0, len(G.graph['colour_map'])):
            if G.graph['colour_map'][j] == None:
                G.graph['colour_map'][j] = random.choice(colours_to_use)
        print(G.edges())
        print(G.graph['colour_map'])
        # print(G.graph['dominating_vertices'])
        try:
            func_return_output = algorithm1(G)
        except:
            continue
        x_axis.append(w)
        output = func_return_output[0]
        print('Output: ' + str(output.edges()))
        matching_time = func_return_output[1]
        entire_alg_time = func_return_output[2]
        alg_excluding_max_matching = func_return_output[3]
        y_axis_entire_program.append(entire_alg_time)
        y_axis_alg_excluding_matching.append(alg_excluding_max_matching)
        y_axis_proposed_big_o.append(max((w*G.number_of_edges()*fixed_num_nodes*fixed_num_nodes), (fixed_num_nodes*(fixed_num_nodes+G.number_of_edges()))))

    plt.plot(x_axis, y_axis_entire_program, 'o')
    plt.xlabel('Number of Colours')
    plt.ylabel('Total Program Run time')
    plt.title('No. colours vs total program run time, no. nodes= ' + str(fixed_num_nodes) + ' , no. edges: ' + str(G.number_of_edges()))
    plt.show()

    # plt.plot(x_axis, y_axis_alg_excluding_matching)
    # plt.xlabel('Number of Colours')
    # plt.ylabel('Program Run time (exc. max matching)')
    # plt.title('Number of colours vs run time exc. max matching')
    # plt.show()

    plt.plot(x_axis, y_axis_proposed_big_o, 'o')
    plt.xlabel('Number of Colours')
    plt.ylabel('Proposed Big-O function')
    plt.title('No. colours vs proposed big-o function, no. nodes= ' + str(fixed_num_nodes) + ' , no. edges: ' + str(G.number_of_edges()))
    plt.show()


def user_interface_mode():
    while True:
        num_isolating = int(input('How many isolated vertices do you wish for the graph to contain?\n'))
        num_dominating = int(input('How many dominating vertices do you wish for the graph to contain?\n'))
        num_colours = int(input('How many unique colours do you wish for the graph to contain? Please enter a number between 1 and ' + str(num_isolating+num_dominating) + ' inclusive\n'))
        G = generate_graph(num_dominating,num_isolating,num_colours)
        try:
            func_return_output = algorithm1(G)
        except:
            continue
        output = func_return_output[0]
        print('Maximum Colourful Cycle: ' + str(output.edges()))
        for e in G.edges():
            G[e[0]][e[1]]['color'] = 'grey'
        for edge in output.edges():
            G[edge[0]][edge[1]]['color'] = 'red'
        # Store in a list to use for drawing
        edge_color_list = [G[e[0]][e[1]]['color'] for e in G.edges()]
        pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())), iterations=20)
        nx.draw(G, node_color=G.graph['colour_map'], nodelist=sorted(list(G.nodes())), edge_color = edge_color_list, with_labels = True, pos=pos)
        plt.show()
        
    
varying_colours()
