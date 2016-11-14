# 6.0002 Problem Set 5
# Graph optimization
# Name: Yun Chang
# Collaborators: None
# Time: 3 hrs

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#The graph's nodes in this case represents the buildings and 
#the edges reoresent the paths and connections to different 
#buildings.The distances are represented in the weights of 
#the edges. (there are two weights, one represents the actual 
#distance, the other represents outdoor distance).


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
    print("Loading map from file...")
    Map = Digraph()
    datafile = open(map_filename, 'r')
    #loop over each line to collect data
    # source destination total_dist outdoor_dist
    for line in datafile:
        map_info = line.split()
        #add source as a node
        source = Node(map_info[0])
        if not Map.has_node(source):
            Map.add_node(source)
        #add destination as a node
        destination = Node(map_info[1])
        if not Map.has_node(destination):
            Map.add_node(destination)
        total_dist = int(map_info[2]) #want the distances to be integers 
        outdoor_dist = int(map_info[3])
        #create the edge from source to destination
        map_edge = WeightedEdge(source,destination,total_dist,outdoor_dist)
        Map.add_edge(map_edge)
    datafile.close()
    return Map 

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#test_map = load_map('test_load_map.txt')
#print (str(test_map))

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: The constraints are the distance spent outdoors and the objective 
#function is to find a path from start to end that traverses the minimum 
#distance required. 

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO
    #use dynamic programming and recursion 
    #return none if all possible choice exceeds max_dist of max_outdoor_dist
    #update path 
    path[0] = path[0] + [start]
    #Initialize Start and End both as Nodes
    start_n = Node(start)
    end_n = Node(end)
    if not digraph.has_node(start_n) or not digraph.has_node(end_n):
        raise ValueError('invalid start or end node')
    elif start == end: #when reaches destination is when recusion should stop
        return (path[0],path[1])
    else:
        for edge in digraph.get_edges_for_node(start_n):
            next_node = Node(edge.get_destination())
            next_node_tot_dist = edge.get_total_distance()
            next_node_out_dist = edge.get_outdoor_distance()
            #get next node, total dist, and outdoor dist 
            #make sure doesn't cycle i.e. come back to same node 
            if next_node.get_name() not in path[0]:
                #check if max outdoor dist exceeded 
                if next_node_out_dist + path[2] <= max_dist_outdoors:
                    #only have to keep going if path is going to be shorter than current best path
                    if best_path == None or next_node_tot_dist + path[1] < best_dist:
                        path_update = [path[0].copy(), path[1]+next_node_tot_dist, path[2]+next_node_out_dist]
                        #updating original path with [list of node, total distance travelled, total dist outdoors]
                        #note that path[0] not updated here but rather within recursive function due to conderation of starting conditions
                        #the "start" parameter of get_best_path function is str, not Node object. 
                        next_path = get_best_path(digraph, next_node.get_name(), end, path_update, max_dist_outdoors, best_dist, best_path)
                        #if all condition satisfied, traverse to next node
                        if next_path != None:
                            best_path = next_path 
                            best_dist = next_path[1]
        return best_path 

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    start_path = [[],0,0]
    shortest_path = get_best_path(digraph, start, end, start_path, max_dist_outdoors, None, None)
    if shortest_path == None: #get_best_path returns None if no possible path/only possible paths exceeds max_dist_outdoors
        raise ValueError('No feasible path')
    elif shortest_path[1] > max_total_dist:
        raise ValueError('Exceeds Maximum total distance')
    else:
        return shortest_path[0]

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()