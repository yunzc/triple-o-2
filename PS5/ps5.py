# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    list_of_models = []
    for degree in degs:
        model = pylab.polyfit(x, y, degree) 
        #polyfit takes arguments of (x-coordinates, y-coordinates, degree of polynomial fit)
        list_of_models.append(model)
    return list_of_models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    y_mean = pylab.mean(y)
    #R^2 = 1 - sum((y_i-e_i)^2)/sum((y_i-y_mean)^2)
    #first calculate sum of (y_i - e_i)^2
    y_minus_e = y - estimated #list of y_i - e_i 
    y_minus_e_sq = y_minus_e**2 #list of (y_i - e_i)^2
    numerator = pylab.sum(y_minus_e_sq) #the numerator term sum((y_i-e_i)^2)
    #next calculate sum of (y_i - y_mean)^2
    y_minus_mean = y - y_mean #list of y_i - y_mean
    y_minus_mean_sq = y_minus_mean**2 #list of (y_i - y_mean)^2
    denom = pylab.sum(y_minus_mean_sq) #the denominator term sum((y_i-y_mean)^2)
    R_sq = 1 - numerator/denom
    return R_sq
    

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #one figure for each model
    for model in models:
        #generate the values as obtained from the model
        estim_val = pylab.polyval(model, x)
        #calculate R^2 
        r_sq = r_squared(y, estim_val)
        degree_model = len(model)-1
        #create title 
        title_str = 'Degree: '+str(degree_model)+'\n R-square = '+str(r_sq)
        if degree_model == 1: #if linear, include SE/slope
            SE_slope = se_over_slope(x, y, estim_val, model)
            title_str += '\n SE/slope = '+str(SE_slope)
        #make plot 
        pylab.figure() #generate figure for each model 
        pylab.plot(x, y, marker='.', color='b', linestyle='None')
        #plot data points with dots that are blue with no lines 
        pylab.plot(x, estim_val, color='r', linestyle='-')
        #plot best fit curve with a red solid line 
        pylab.title(title_str)
        pylab.xlabel('year')
        pylab.ylabel('temperature (Celsius)')

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    
    avg_temp_list = [] #list of the average temperature each year
    for year in years: 
        temp_sum_over_cities = 0 #total sum of all the average temperature of each city 
        for city in multi_cities:
            #get an array of the temperatures at this city and year 
            year_temps = climate.get_yearly_temp(city, year) 
            avg_year_temp = pylab.average(year_temps) #find year average of this city 
            temp_sum_over_cities += avg_year_temp
        #average the yearly averages from each city 
        avg_over_cities = temp_sum_over_cities/len(multi_cities) 
        avg_temp_list.append(avg_over_cities)
    return pylab.array(avg_temp_list) #return pylab 1-d array

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    mov_avg_list = [] #create list to store moving average 
    for i in range(len(y)):
        if i < window_length - 1: #when we don't have enough previous value 
            ith_avg = pylab.average(y[:i+1]) #average current value with previous values
            mov_avg_list.append(ith_avg)
        else: 
            ith_avg = pylab.average(y[i+1-window_length:i+1])#average of the values in window
            mov_avg_list.append(ith_avg)
    mov_avg = pylab.array(mov_avg_list) #convert to array 
    return mov_avg
            

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    #rmse = (sum((y_i-estim_i)^2)/n)^(1/2)
    #first creat array of terms (y_i - estim_y)^2
    diff_sq = (y - estimated)**2
    sum_diff_sq = pylab.sum(diff_sq)
    rmse = (sum_diff_sq/len(y))**(0.5) 
    return rmse 

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std_dev_list = []
    for year in years: 
        daily_sum = 0
        #sum up the daily temperatures for each city 
        for city in multi_cities:
            daily_sum += climate.get_yearly_temp(city, year)
        daily_avg = daily_sum/len(multi_cities) #average across the cities 
        #standard deviations of the daily averages for the whole year
        std_dev = pylab.std(daily_avg) 
        std_dev_list.append(std_dev) #add to list 
    return pylab.array(std_dev_list) # return array of the list 

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #one figure for each model
    for model in models:
        #generate the values as obtained from the model
        estim_val = pylab.polyval(model, x)
        #calculate R^2 
        rm_se = rmse(y, estim_val)
        degree_model = len(model)-1
        #create title 
        title_str = 'Degree: '+str(degree_model)+'\n RMSE = '+str(rm_se)
        #make plot 
        pylab.figure() #generate figure for each model 
        pylab.plot(x, y, marker='.', color='b', linestyle='None')
        #plot data points with dots that are blue with no lines 
        pylab.plot(x, estim_val, color='r', linestyle='-')
        #plot best fit curve with a red solid line 
        pylab.title(title_str)
        pylab.xlabel('year')
        pylab.ylabel('temperature (Celsius)')

if __name__ == '__main__':
    climate_data = Climate('data.csv') #initialize data 
    # Part A.4
    years = pylab.array(TRAINING_INTERVAL) #the x values of the dataset 
    temp_list = [] #use climate class to obtain the temperature on Jan 10th in NYC that year 
    for year in TRAINING_INTERVAL:
        temp_list.append(climate_data.get_daily_temp('NEW YORK', 1, 10, year))
    temp = pylab.array(temp_list) #array of temperature (y) values 
    models = generate_models(years, temp, [1]) #fit to degree one 
    evaluate_models_on_training(years, temp, models) #plot AI
    #now want annual temperature 
    ann_temp_list = [] #use climate data to obtain annual average temperature 
    for year in TRAINING_INTERVAL:
        year_temperatures = climate_data.get_yearly_temp('NEW YORK', year)
        average_year_temp = pylab.average(year_temperatures)
        ann_temp_list.append(average_year_temp)
    ann_temp = pylab.array(ann_temp_list)
    models_ann = generate_models(years, ann_temp, [1])
    evaluate_models_on_training(years, ann_temp, models_ann) #plot AII
    # Part B 
    #national yearly temperatures 
    #get national average temperature in the years 
    nat_avg_temp = gen_cities_avg(climate_data, CITIES, TRAINING_INTERVAL)
    #generate model 
    nat_temp_model = generate_models(years, nat_avg_temp, [1]) #fit with deg 1
    evaluate_models_on_training(years, nat_avg_temp, nat_temp_model) #plot B
    # Part C
    #take moving average of national average temperature 
    mov_nat_temp = moving_average(nat_avg_temp, 5) #window size of 5 on the national temperatures
    mov_nat_model = generate_models(years, mov_nat_temp, [1]) #fit with deg 1 
    evaluate_models_on_training(years, mov_nat_temp, mov_nat_model) # plot C
    # Part D.2
    # predicting 
    #Problem 2. I
    #from the previous parts mov_nat_temp is the 5 yr moving averages from 1961-2009
    #fit data to degree 1, 2, and 20
    data_models = generate_models(years, mov_nat_temp, [1, 2, 20])
    evaluate_models_on_training(years, mov_nat_temp, data_models) #plot
    #Problem 2.II
    #define the array for years 2010-2015 
    test_years = pylab.array(TESTING_INTERVAL)
    #find 5 year moving average from 2010- 2015
    #get national average temperature in the years 
    avg_temp_D = gen_cities_avg(climate_data, CITIES, TESTING_INTERVAL)
    #take moving average of national average temperature 
    move_avg_D = moving_average(avg_temp_D, 5)
    #plot to compare models obtained from years 1961-2009
    evaluate_models_on_testing(test_years, move_avg_D, data_models)
    # Part E
    # TODO: replace this line with your code
    #standard deviation of all 21 cities over 1961 to 2009 
    std_dev_years = gen_std_devs(climate_data, CITIES, years)
    #5 year moving averages on the standard deviations 
    mov_std_dev = moving_average(std_dev_years, 5)
    #fit data to degree one polynomial 
    std_dev_model = generate_models(years, mov_std_dev, [1]) #degree one
    evaluate_models_on_training(years, mov_std_dev, std_dev_model) #plot 