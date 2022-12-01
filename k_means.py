import math 
import random 
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
plt.style.use('ggplot')

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
        self.clusters = None # Hashmap: Key = cluster number, Value = list of DataPoints in cluster  
        # SETUP 
        # Read the data file into training_data list and find percent and volitility means 
        self.read_data(in_file)
        # Find standard deviations for percent and volatility 
        self.set_standard_deviations()
        # Find the z-scores for percent and volatility (scales the features)
        self.set_point_zScores()
        # Use z-score scaling 
        self.use_scaling()                  
        # Choose centers
        #self.initialize_centers_random()
        self.initialize_centers_with_data()
        
        
    """
    Applies z-score scaling to the data
    Changes percent and volatility attributes to z-score values for each attribute 
    """
    def use_scaling(self): 
        for data_point in self.training_data: 
            data_point.percent = data_point.p_zScore
            data_point.volatility = data_point.v_zScore
                   
                    
    """
    Removes outliers from training data (ended up not using this)
    """
    def remove_outliers(self): 
        new_data = []
        for data_point in self.training_data: 
            if data_point.percent < 30: 
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
    Assignes a single data point to the closest cluster in the list of clusters
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
            percent_sums[data_point.cluster] += data_point.percent 
            volatility_sums[data_point.cluster] += data_point.volatility 
            counts[data_point.cluster] += 1
        # Find means and readjust centers 
        for cluster_number in range(0, len(self.centers)):             
            if counts[cluster_number] != 0:
                percent_mean = percent_sums[cluster_number] / counts[cluster_number] 
                volatility_mean = volatility_sums[cluster_number] / counts[cluster_number] 
                # Check for centroid convergence 
                if self.centers[cluster_number].percent == percent_mean and \
                    self.centers[cluster_number].volatility == volatility_mean: 
                    done_clustering = True 
                else: 
                    done_clustering = False
                    self.centers[cluster_number].percent = percent_mean  
                    self.centers[cluster_number].volatility = volatility_mean 
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
            #self.display_clusters()
        # Store data points in each cluster 
        self.clusters = {i:[] for i in range(0, self.k)} # Key = cluster number, Value = list of DataPoints in cluster 
        for data_point in self.training_data:
            # Store points in each cluster
            self.clusters[data_point.cluster].append(data_point)
                                                    
                
    """
    Displays clusters on a scatterplot using matplot lib 
    Displays axes in terms of non-scaled percent and volatility
    """
    def display_clusters(self): 
        plt.figure(figsize=(13, 7))
        colors = ["#fc543a", "#6fa8dc", "#93c47d", "#ff9566", "#ffd966", "pink", "grey", "yellow", "brown", "violet"] 
        clusters = {} # Key = cluster number, Value = list of DataPoints in cluster 
        for data_point in self.training_data: 
            # Store points in each cluster 
            if data_point.cluster not in clusters: 
                clusters[data_point.cluster] = []
            clusters[data_point.cluster].append(data_point)
            
        # Plot each cluster
        for cluster in clusters: 
            data_points = clusters[cluster]
            percents = []
            volatilities = []
            for data_point in data_points: 
                # Convert features back back to original unscaled values
                percents.append(100*((data_point.percent * self.percentSD) + self.percentMean))
                volatilities.append((data_point.volatility * self.volatilitySD) + self.volatilityMean)            
            plt.scatter(percents, volatilities, color=colors[cluster], alpha = 0.8)
         
        # Plot the centroids
        center_percents = []
        center_volatilites = []
        for center in self.centers: 
            # Convert features back to original unscaled values
            center_percents.append(100*((center.percent * self.percentSD) + self.percentMean))
            center_volatilites.append((center.volatility * self.volatilitySD) + self.volatilityMean)
        plt.scatter(center_percents, center_volatilites, color = "black", marker="x")    
        
        # Label graph
        plt.xlabel('Percent Gain', fontsize=15)
        plt.ylabel('Volatility', fontsize=15)
        plt.title('k-Means Cluster Analysis Results\n', loc='left', fontsize=22)
        
        # Add a legend
        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Cluster {}'.format(i+1), 
        markerfacecolor=colors[i], markersize=10) for i in range(0, self.k)]
        plt.legend(handles=legend_elements, loc='upper right',  prop={'size':15})      
        plt.show()
        
        
    """
    Returns a hash map representing all clusters: 
          Key = cluster number
          Value = list of DataPoints in cluster 
    """    
    def get_clusters(self): 
        clusters = {i:[] for i in range(0, self.k)} # Key = cluster number, Value = list of DataPoints in cluster 
        for data_point in self.training_data:
            # Store points in each cluster
            clusters[data_point.cluster].append(data_point)
        return clusters
            
            
    """
    Writes the tickers in each cluster to a file (so it can be stored and analyzed)
    Displays a bar graph representing the number of DataPoints in each cluster
    """
    def show_cluster_points(self): 
        self.get_clusters() # Get data points in each cluster 
        # Write each ticker to the file
        out_file = open("resulting_clusters.txt", "w")
        for cluster_num in self.clusters.keys(): 
            data_points = self.clusters[cluster_num]
            to_write = "CLUSTER: " + str(cluster_num + 1) + "\n"
            for data_point in data_points: 
                to_write += data_point.ticker + "\n"            
            out_file.write(to_write)
        
        # Create a bar graph to show how many points are in each cluster
        cluster_nums = []
        cluster_counts = []
        for cluster_num in range(0, self.k): 
            count = len(self.clusters[cluster_num])
            c_num = cluster_num + 1
            cluster_nums.append("Cluster " + str(c_num))
            cluster_counts.append(count)
        plt.figure(figsize = (10, 5))
        plt.bar(cluster_nums, cluster_counts, width = 0.4, color = ["#fc543a", "#6fa8dc", "#93c47d", "#ff9566"], alpha=0.5) 
        for i in range(len(cluster_nums)): 
            plt.text(i, cluster_counts[i], cluster_counts[i])
        plt.xlabel("Cluster")
        plt.ylabel("Number of Stocks in Cluster")
        plt.title("Number of Stocks in Each Cluster") 
        plt.show()

        
# Runs k-means given the number of clusters and the stock data file      
def main(): 
    # Our Final Model Setup: 
    # Seed choice: random data points 
    # K = 4
    # Feature scaling: z-score
    # No removal of outliers 
    my_clusterer = kMeansClusterer(4, "newData.txt")
    my_clusterer.cluster()
    my_clusterer.display_clusters()
    my_clusterer.show_cluster_points()
        
if __name__ == "__main__":    
    main()