###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    if target_weight in egg_weights:#if target weight identical to the weight of any of the eggs, just need that one egg 
        return 1
    elif target_weight in memo.keys(): #take from memo is value is known 
        return memo(target_weight)
    else: #when value has not yet been calculated and is not identical to weight of any of the eggs 
        #find the largest egg that can fit 
        egg_weights_sorted = sorted(egg_weights, reverse=True) #try largest value first 
        heaviest_possible = 0
        for weight in egg_weights_sorted:
            if weight < target_weight:
                heaviest_possible = weight 
                break
        """least number of eggs is the least number of eggs for the weight of the heaviest egg possible subtracted 
        from the target weight"""
        least_possible_eggs = 1 + dp_make_weight(egg_weights ,target_weight - heaviest_possible, memo = {}) 
        memo[target_weight] = least_possible_eggs #add new value to memo 
        return least_possible_eggs


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()