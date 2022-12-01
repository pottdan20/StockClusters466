import k_means 
from matplotlib import pyplot as plt
import math

"""
Finds the optimal k for k-means clustering using silhouette analysis 
The silhouette coefficient (of a single point) is a measure of how similar a data point is within a cluster (cohesion)
compared to other clusters (separation)

Algorithm: 
- Select range of values for k: (1...n)
- Plot mean silhouette coefficient for each k
- Optimal k = maximum of plot 
"""
class silhouetteMethod(): 
    def __init__(self, k_start, k_end):
        self.k_start = k_start
        self.k_end = k_end 
        self.clusterer = None # Clusterer object used for k-means 
        self.clusters = None # Hashmap: key = cluster number, value = list of DataPoints in cluster 
    
    
    """
    Returns the optimal number of clusters by finding the silhouette coefficient 
    The silhouette coefficient corresponds to the optimal K 
    SC = max {mean_S for all k}
    """
    def find_optimal_k(self): 
        silhouette_values = [] # Mean silhouette values for each value of k 
        k_values = [i for i in range(self.k_start, self.k_end+1)] # Values of k 
        silhouette_coefficient = -2 
        best_k = 0 
        for k in range(self.k_start, self.k_end+1):     
            self.clusterer = k_means.kMeansClusterer(k, "newData.txt")
            self.clusterer.cluster() # Cluster the data into k clusters
            self.clusters = self.clusterer.clusters # Get the points in each cluster 
            avg_silhouette = self.calculate_avg_silhouette() # Find the avg. silhouette for current clustering 
            # Keep track of max avg. silhouette (and corresponding k)
            if avg_silhouette > silhouette_coefficient: 
                silhouette_coefficient = avg_silhouette 
                best_k = k
            silhouette_values.append(avg_silhouette)
            print("K = " + str(k) + ", " + "AVG SILHOUETTE: " + str(avg_silhouette))
        print("SILHOUETTE COEFFICIENT: " + str(silhouette_coefficient))        
        print("OPTIMAL K: " + str(best_k))
        print()
        # Plot silhouette graph
        plt.plot(k_values, silhouette_values)
        plt.xlabel("K")
        plt.ylabel("Average Silhouette Value")
        plt.title("Silhouette Analysis for K-Means Clustering")
        plt.show()


    """
    Calculates the avg. silhouette value for a single clustering (single k value)
    The avg S(i) over all points of a cluster shows how well that cluster has been clustered, 
    so the avg S(i) over all data points shows how well the entire data has been clustered 
    
    avg_silhouette = mean{s(i)} for all i (all data points)
    """
    def calculate_avg_silhouette(self): 
        silhouette_sum = 0 
        count = 0
        # Calculate silhouette for value for each data point, then compute average 
        for i in self.clusterer.training_data: 
            silhouette_sum += self.calculate_S(i)
            count += 1
        avg_silhouette = silhouette_sum / count 
        return avg_silhouette 
    
    
    """
    Calculates S(i), where i is a single data point
    S(i) = the silhouette value of data point i
    Formula: S(i) = b(i) - a(i) / max{a(i), b(i)} if |CI| > 1
             S(i) = 0 if |CI| = 1 
    The range of S(i) is: [-1, 1] 
        S(i) close to 1: point is clustered well (more similarity)
        S(i) close to -1: point is clustered poorly (more dissimilarity, point would be better in neighboring cluster)
        S(i) close to 0: point is on boarder of two clusters
    """
    def calculate_S(self, i):
        if len(self.clusters[i.cluster]) == 1: #CHECK FOR LEN == 0 
            return 0 
        else: 
            a = self.calculate_a(i)
            b = self.calculate_b(i)
            S = (b - a) / (max(a, b))
            return S    
    
    
    """
    Calculates a(i), where i is a single data point belonging to CI
    a(i) = the avg. distance between i and all other data points in the cluster CI that i belongs to
    """
    def calculate_a(self, i): 
        distance_sum = 0 # Sum of distances between i and all other data_points in CI
        cluster_num = i.cluster # The number corresponding to the cluster that i is in, CI
        count = len(self.clusters[cluster_num]) # The number of data points in CI 
        for data_point in self.clusters[cluster_num]: 
            # Find the distance between each point in CI and i 
            dist_sq = math.pow((data_point.percent - i.percent), 2) + \
                math.pow((data_point.volatility - i.volatility), 2)
            distance_sum += dist_sq 
        a = distance_sum / (count-1) # divide by count-1 since we don't include i  
        return a


    """
    Calculates b(i), where i is a single data point belonging to CI
    b(i) = the min {avg. distance from i to all points in CJ} for all J != I
    (the cluster with the smallest mean dissimilarity it the "neighboring cluster" of I)
    """
    def calculate_b(self, i): 
        min_avg = float('inf') # minimum avg. distance from i to all points in a neighboring cluster 
        i_cluster_num = i.cluster # The number corresponding to the cluster that i is in, CI
        # Look at all other clusters that i is not in
        for other_cluster_num in range(0, self.clusterer.k):
            if other_cluster_num != i_cluster_num:
                # i is not in the cluster 
                distance_sum = 0 
                count = len(self.clusters[other_cluster_num]) # The number of data points in CJ
                for data_point in self.clusters[other_cluster_num]: 
                    # Find the distance between each point in CJ and i 
                    dist_sq = math.pow((data_point.percent - i.percent), 2) + \
                        math.pow((data_point.volatility - i.volatility), 2)            
                    distance_sum += dist_sq
                curr_avg = distance_sum / count
                min_avg = min(curr_avg, min_avg) # update min avg and move on to next cluster
        return min_avg 
                               

# Performs silhouette analysis to find the optimal k by testing k in a given range 
def main(): 
    print()
    k_finder = silhouetteMethod(2, 8)
    k_finder.find_optimal_k()

if __name__ == "__main__": 
    main()