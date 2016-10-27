###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    #create dictionary to place files in
    cow_dictionary = {}
    #read data 
    datafile = open(filename, 'r')
    #loop over each line to collect data 
    for line in datafile:
        #split each line to [name, weight]
        cow_info = line.split(',')
        #append each cow into cow_dictionary 
        cow_dictionary[cow_info[0]]=int(cow_info[1])
    return cow_dictionary

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    #make list of cows that is sorted by weight (decresasing)
    cows_list = sorted(cows, key=cows.__getitem__, reverse=True)
    transport_list = []
    #loop until all the cows are transported 
    while len(cows_list)>0:
        trip_weight = 0 
        item_for_trip = []
        #going from heavier to lighter, add the cows that still fit
        for cow in cows_list:
            if (trip_weight + cows[cow] <= limit):
                item_for_trip.append(cow)
                trip_weight += cows[cow]
        transport_list.append(item_for_trip)
        #remove the transported cows from list 
        for transported_cow in item_for_trip:
            cows_list.remove(transported_cow)
    return (transport_list)

        
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here 
    cow_list = cows.keys()
    final_trip_plan = []
    #partition cows and iterate over different partitions -- starting with one partition (one trip) and increasing
    for trip_plan in get_partitions(cow_list):
        #check weight for each trip: if weight exceeds limit, overweight = 0
        overweight = 1  
        for trip in trip_plan:
            trip_weight = 0
            for cow in trip:
                trip_weight += cows[cow]
            if trip_weight > limit:
                overweight *= 0
                break #if one trip overweight, trip plan invalid
        if overweight == 1: #find the first viable trip plan with least partition 
            final_trip_plan = trip_plan
            break
    return (final_trip_plan)
  
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows('ps1_cow_data.txt')
    start1 = time.time() #take note of start time
    greedy_plan = greedy_cow_transport(cows)
    end1 = time.time() #end time when finish with greedy algo
    greedy_time = end1 - start1
    greedy_num_trips = len(greedy_plan) #length of plan list is the number of trips
    start2 = time.time() #start time for greedy 2
    brutey_plan = brute_force_cow_transport(cows)
    end2 = time.time() #end time upon completion of brute force algo 
    brutey_time = end2 - start2
    brutey_num_trips = len(brutey_plan)
    print ('Greedy algorithm planed %s trips' % str(greedy_num_trips))
    print ('Greedy algorithm took %s seconds' % str(greedy_time))
    print ('Brute Force algorithm planed %s trips' % str(brutey_num_trips))
    print ('Brute Force algorithm took %s seconds' % str(brutey_time))

compare_cow_transport_algorithms()

