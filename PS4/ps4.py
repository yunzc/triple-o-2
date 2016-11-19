# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random


##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        self.birth_prob = birth_prob
        self.death_prob = death_prob

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        #randomly generate probability to decide its fate 
        fate = random.random()
        return fate < self.death_prob
    

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        #generate random float to decide if the time is right for reproduction 
        time_is_right = random.random()
        if time_is_right < self.birth_prob * (1 - pop_density):
            offspring = SimpleBacteria(self.birth_prob, self.death_prob)
            return offspring 
        else:
            raise NoChildException #the time is not right => no child :( 


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        return len(self.bacteria) #number of SimpleBacteria

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        survivors = [] #list of surviving bacterias smiled upon by fate
        for cell in self.bacteria:
            if not cell.is_killed(): #survived
                survivors.append(cell) 
        popul_density = len(survivors)/self.max_pop #current population density
        babies = [] #newly reproduced bacteria cells
        for surviving_cell in survivors:
            try:
                baby = surviving_cell.reproduce(popul_density)
                babies.append(baby)
            except NoChildException: #nothing happens, no new child 
                pass
        self.bacteria = survivors + babies
        return len(self.bacteria) #total bacteria at the end of the day 



##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    sum_for_all_trials = 0
    num_trials = len(populations) #number of trials
    for trial in range(num_trials):
        sum_for_all_trials += populations[trial][n] #obtain value for time step n
    return sum_for_all_trials/num_trials #take average 


def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    populations = [] #record data over trials 
    for trial in range(num_trials):
        bacteria_list = [SimpleBacteria(birth_prob, death_prob)]*num_bacteria
        patient = Patient(bacteria_list, max_pop)
        timestep = 0
        trial_data = [] #data for this trial
        while timestep < 300:
            trial_data.append(patient.get_total_pop())
            patient.update()
            timestep += 1
        populations.append(trial_data) #adding data from trial to main data matrix 
    avg_populations = []
    for timestep in range(300):
        avg_pop_size = calc_pop_avg(populations,timestep) #calculate avg population size
        avg_populations.append(avg_pop_size) 
    make_one_curve_plot(range(1,301), avg_populations, 'Timesteps', 'Population size', 'No Antibiotic Treatment') #time step 1 to 300
    return populations 



# When you are ready to run the simulation, uncomment the next line
#populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    num_trials = len(populations)
    avg_pop_t = calc_pop_avg(populations, t)
    sum_sq_dist = 0 #find sum of squared distance from average 
    for trial in range(num_trials):
        sq_dist = (populations[trial][t] - avg_pop_t)**2
        sum_sq_dist += sq_dist
    return (sum_sq_dist/num_trials)**(0.5) #square root of average squared distance

def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    num_trials = len(populations)
    avg_pop_t = calc_pop_avg(populations, t)
    std_dev_t = calc_pop_std(populations, t)
    std_error_t = std_dev_t/(num_trials)**0.5
    return (avg_pop_t, 1.96 * std_error_t)
    


##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        SimpleBacteria.__init__(self, birth_prob, death_prob)
        self.resistant = resistant 
        self.mut_prob = mut_prob

    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        fate = random.random() #see if bacteria is ready to go to heaven/hell
        if self.get_resistant():
            return fate < self.death_prob #dies with regular death probability
        else:
            return fate < self.death_prob/4 #dies with regular death probability /4
            
    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        #generate random float to decide if the time is right for reproduction 
        time_is_right = random.random()
        if time_is_right < self.birth_prob * (1 - pop_density): #reproduces! 
            mut_chance = random.random() 
            #offspring has probability of mut_prob * (1- pop_density) to develop resistant trait 
            #if parent has antibiotic resistance, offspring also
            if self.get_resistant() or mut_chance < self.mut_prob * (1 - pop_density): #offspring has resistance 
                offspring = ResistantBacteria(self.birth_prob, self.death_prob, True, self.mut_prob)
                #has same birth, death, mut probability , and resistance 
            else: #offspring does not develop resistance
                offspring = ResistantBacteria(self.birth_prob, self.death_prob, False, self.mut_prob)
            return offspring 
        else:
            raise NoChildException #the time is not right => no child :( 


class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        Patient.__init__(self, bacteria, max_pop)
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self.on_antibiotic = True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        num_with_resistance = 0
        for cell in self.bacteria: 
            if cell.get_resistant():
                num_with_resistance += 1
        return num_with_resistance

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        survivors = [] #list of surviving bacterias smiled upon by fate
        for cell in self.bacteria:
            if not cell.is_killed(): #did not die
                survivors.append(cell) 
        if self.on_antibiotic: #patient on antibiotics
            for candidate_cells in survivors:
                if not candidate_cells.get_resistant(): #not resistant to antibiotics 
                    survivors.remove(candidate_cells)
        popul_density = len(survivors)/self.max_pop #current population density
        babies = [] #newly reproduced bacteria cells
        for surviving_cell in survivors:
            try:
                baby = surviving_cell.reproduce(popul_density)
                babies.append(baby)
            except NoChildException: #nothing happens, no new child 
                pass
        self.bacteria = survivors + babies
        return len(self.bacteria) #total bacteria at the end of the day 


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    total_pop = [] #total number of bacteria total_pop[trial][timestep]
    resistant_pop = [] #number of resistant bacteria resistant_pop[trial][timestep]
    for trial in range(num_trials):
        #initialize list of resistant bacteria according to num bacteria 
        bacteria_list = [ResistantBacteria(birth_prob, death_prob, resistant, mut_prob)]*num_bacteria
        #initialize patient     
        patient = TreatedPatient(bacteria_list, max_pop)
        ts_no_antibiotic = 0
        trial_data_tot = [] #total bacteria data for this trial
        trial_data_res = [] #data for resistant bacteria data 
        #150 time steps of no antibiotic
        while ts_no_antibiotic < 150:
            trial_data_tot.append(patient.get_total_pop())
            trial_data_res.append(patient.get_resist_pop())
            patient.update()
            ts_no_antibiotic += 1
        #add antibiotic 
        patient.set_on_antibiotic()
        ts_w_antibiotic = 0
        #run 250 with antibiotic 
        while ts_w_antibiotic < 250:
            trial_data_tot.append(patient.get_total_pop())
            trial_data_res.append(patient.get_resist_pop())
            patient.update()
            ts_w_antibiotic += 1
        total_pop.append(trial_data_tot) #adding data from trial to main data matrix for total bacteria population
        resistant_pop.append(trial_data_res) #addig data from trial to resistant bacteria data matrix
    avg_pop_tot = [] #total bacteria averaging over trials
    avg_pop_res = []#resistant bacteria 
    for timestep in range(400):
        avg_pop_size_tot = calc_pop_avg(total_pop, timestep) #calculate avg population size for total for timestep
        avg_pop_size_res = calc_pop_avg(resistant_pop, timestep) #calculate avg for resistant 
        avg_pop_tot.append(avg_pop_size_tot) 
        avg_pop_res.append(avg_pop_size_res)
    #time step 1 to 150+250
    make_two_curve_plot(range(1,401), 
                        avg_pop_tot, 
                        avg_pop_res, 
                        'Total', 
                        'Resistant',
                        'Timesteps', 
                        'Average population', 
                        'With Antibiotic Treatment')     
    return (total_pop, resistant_pop)

# When you are ready to run the simulations, uncomment the next lines one
# at a time
total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100, 
                                                      max_pop=1000,
                                                      birth_prob=0.3,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)
#
#total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                      max_pop=1000,
#                                                      birth_prob=0.17,
#                                                      death_prob=0.2,
#                                                      resistant=False,
#                                                      mut_prob=0.8,
#                                                      num_trials=50)

tot_95_ci = calc_95_ci(total_pop, 299)
res_95_ci = calc_95_ci(resistant_pop, 299)
print ('95 % confidence interval for total population estimate: ', tot_95_ci)
print ('95 % confidence interval for resistant population estimate: ', res_95_ci)