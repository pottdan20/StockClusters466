import math 
import random 
from matplotlib import pyplot as plt
import numpy as np

"""
Represents a single data point to be clustered 
"""
class DataPoint: 
    def __init__(self, ticker, percent, volatility): 
        self.ticker = ticker  # String ticker 
        self.percent = percent # Percent gain in stock for the year
        self.volatility = volatility # Volatility of the stock for the year 
        self.cluster = None # The number corresponding to the cluster the point is in 
        self.p_zScore = None # The z_score value of the percent gain 
        self.v_zScore = None # The z_score value of the volatility 

    def __repr__(self):
        return '(' + self.ticker + ', ' + \
            str(round(self.percent, 3)) + ', ' + \
                str(round(self.volatility, 3)) + ', ' + \
                    str(self.cluster) + ')'

    def __eq__(self, other): 
        return type(other) == DataPoint and \
            self.ticker == other.ticker and \
                self.percent == other.percent and \
                    self.volatility == other.volatility                      


"""
Performs K-Means clustering on data in in_file
Displays clusters on a graph
"""
class kMeansClusterer:
    def __init__(self, k, in_file):
        self.k = k # Number of clusters 
        self.training_data = [] # List of data points 
        self.centers = [None for i in range(0, k)] # Index is cluster number, value is data point of center  
        self.percentMean = None 
        self.volatilityMean = None 
        self.percentSD = None
        self.volatilitySD = None    
        # SETUP 
        # Read the data file into training_data list and find percent and volitility means 
        self.read_data(in_file)
        # Find standard deviations for percent and volatility 
        self.set_standard_deviations()
        # Find the z-scores for percent and volatility (scales the features)
        self.set_point_zScores()
        # Use scaling and remove outliers 
        self.use_scaling() 
        self.remove_outliers()              
        # Choose centers 
        self.initialize_centers_random()
        #self.initialize_centers_with_data()
        
        
    """
    Applies z-score scaling to the data
    Changes percent and volatility attributes to z-score values for each attribute 
    """
    def use_scaling(self): 
        for data_point in self.training_data: 
            data_point.percent = data_point.p_zScore
            data_point.volatility = data_point.v_zScore
                    
                    
    """
    Removes outliers from training data
    """
    def remove_outliers(self): 
        new_data = []
        for data_point in self.training_data: 
            if data_point.percent < 6: 
                new_data.append(data_point)
        self.training_data = new_data
            
        
    """
    Reads data file into a list of DataPoint objects 
    Sets the variables for percent and volatility mean 
    """
    def read_data(self, in_file): 
        data_file = open(in_file, 'r')
        percentSum = 0
        volatilitySum = 0
        count = 0
        for line in data_file: 
            line_lst = line.split(" ")
            self.training_data.append(DataPoint(line_lst[0], float(line_lst[1]), float(line_lst[2])))
            percentSum += float(line_lst[1])
            volatilitySum += float(line_lst[2])
            count += 1
        # Set the means 
        self.percentMean = percentSum / count
        self.volatilityMean = volatilitySum / count
        data_file.close()
        
        
    """
    Sets the standard deviation for percent and volatility 
    """
    def set_standard_deviations(self): 
        percentDiffSum = 0
        volatilityDiffSum = 0
        count = 0
        for point in self.training_data:
            count += 1
            percentDiffSum += (point.percent - self.percentMean) ** 2
            volatilityDiffSum += (point.volatility - self.volatilityMean) ** 2
        self.percentSD = math.sqrt(percentDiffSum / (count -1))
        self.volatilitySD = math.sqrt(volatilityDiffSum / (count -1))
        
        
    """
    Calculates the z-score values for percent and volatility
    This is used to scale the features
    """
    def set_point_zScores(self):
        for point in self.training_data:
            point.p_zScore = (point.percent - self.percentMean)/self.percentSD
            point.v_zScore = (point.volatility - self.volatilityMean) / self.volatilitySD
    
    
    """
    Generates k random centers in range of the training data min and max
    """
    def initialize_centers_random(self):
        min_percent = self.training_data[0].percent
        max_percent = self.training_data[0].percent
        min_volatility = self.training_data[0].volatility
        max_volatility = self.training_data[0].volatility
        # Find the min and max for percent and volatility in training data 
        for point in self.training_data:
            if point.percent < min_percent:
                min_percent = point.percent 
            if point.percent > max_percent: 
                max_percent = point.percent 
            if point.volatility < min_volatility: 
                min_volatility = point.volatility 
            if point.volatility > max_volatility: 
                max_volatility = point.volatility
        # Create random centers 
        for i in range(0, self.k):
            name = "CENTER_" + str(i)
            percent = random.randint(int(min_percent), int(max_percent)) # Generate a random percent 
            volatility = random.randint(int(min_volatility), int(max_volatility)) # Generate a random volatility 
            # Create new data point and add to list of centers
            self.centers[i] = DataPoint(name, percent, volatility)
    
    
    """
    Generates k random centers, where each center is a random point in the training data
    """
    def initialize_centers_with_data(self): 
        for i in range(0, self.k): 
            name = "CENTER_" + str(i)
            index = random.randint(0, len(self.training_data)) # Generate a random index to choose a random point in training data
            percent = self.training_data[index].percent
            volatility = self.training_data[index].volatility 
            # Scale the features 
            p_zScore = (percent - self.percentMean) / self.percentSD
            v_zScore = (volatility - self.volatilityMean) / self.volatilitySD
            # Create new data point and add to list of centers
            to_add = DataPoint(name, percent, volatility)
            to_add.p_zScore = p_zScore
            to_add.v_zScore = v_zScore
            self.centers[i] = to_add
            
    
    """
    Assignes a single data point to the closes cluster in the list of clusters
    """
    def assign_to_cluster(self, data_point): 
        # Look at the distance to each cluster center and keep track of minimum 
        min_dist = float('inf')
        min_cluster = 0 
        for i in range(0, len(self.centers)): 
            curr_cluster_center = self.centers[i]
            # Use Euclidean distance metric   
            curr_dist = math.pow((curr_cluster_center.percent - data_point.percent), 2) + \
                math.pow((curr_cluster_center.volatility - data_point.volatility), 2)
            if curr_dist < min_dist: 
                min_dist = curr_dist
                min_cluster = i 
        # Assign data point to the closest cluster
        data_point.cluster = min_cluster 
    
    
    """
    Readjusts cluster centers using avg. of each feature for each point in cluster 
    Returns true if the centers have converged 
    """
    def adjust_centers(self): 
        done_clustering = False  
        # Index = cluster number 
        # Value = sum of percent for each point in that cluster 
        percent_sums = [0 for x in range(0, len(self.centers))] 
        # Index = cluster number 
        # Value = sum of volatility for each point in that cluster 
        volatility_sums = [0 for x in range(0, (len(self.centers)))]
        # Index = cluster number 
        # Value = number of points in that cluster 
        counts = [0 for x in range(0, len(self.centers))]                
        # Find sums 
        for data_point in self.training_data: 
            percent_sums[data_point.cluster] += data_point.percent # HERE !!!
            volatility_sums[data_point.cluster] += data_point.volatility # HERE !!!
            counts[data_point.cluster] += 1
        # Find means and readjust centers 
        for cluster_number in range(0, len(self.centers)):             
            if counts[cluster_number] != 0:
                percent_mean = percent_sums[cluster_number] / counts[cluster_number] # HERE !!!
                volatility_mean = volatility_sums[cluster_number] / counts[cluster_number] # HERE !!!
                # Check for centroid convergence 
                if self.centers[cluster_number].percent == percent_mean and \
                    self.centers[cluster_number].volatility == volatility_mean: # HERE !!!
                    done_clustering = True 
                else: 
                    done_clustering = False
                    self.centers[cluster_number].percent = percent_mean  # HERE !!!
                    self.centers[cluster_number].volatility = volatility_mean # HERE !!!
        return done_clustering 
      
            
    """
    Performs K-means clustering until the centers converge 
    Displays the clusters on a graph 
    """        
    def cluster(self):  
        keep_going = True 
        while keep_going:
            for data_point in self.training_data: 
                self.assign_to_cluster(data_point)
            if self.adjust_centers() == True: 
                keep_going = False
                
                
def main(): 
    my_clusterer = kMeansClusterer(6, "data2021.txt")
    #my_clusterer.initialize_centers_random()   
    #my_clusterer.initialize_centers_with_data()
    my_clusterer.cluster()
    
    colors = ["red", "green", "blue", "pink", "purple", "orange", "yellow", "grey"]
    clusters = {}
    for data_point in my_clusterer.training_data:
        if data_point.cluster not in clusters: 
            clusters[data_point.cluster] = []
        clusters[data_point.cluster].append(data_point)
    for cluster in clusters: 
        data_points = clusters[cluster]
        p = []
        v = []            
        for data_point in data_points: 
            p.append(data_point.percent)
            v.append(data_point.volatility)
        plt.scatter(p, v, color = colors[data_point.cluster], alpha = 0.5)            
    centersp = []
    centersv = []
    for center in my_clusterer.centers: 
        centersp.append(center.percent)
        centersv.append(center.volatility)
    plt.scatter(centersp, centersv, color = "black", alpha = 0.5)            
    plt.show()        

        



    my_clusterer.cluster()
    
if __name__ == "__main__":    
    main()