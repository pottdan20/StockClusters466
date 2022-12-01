import k_means 
from matplotlib import pyplot as plt
import math
plt.style.use('ggplot')

"""
Finds the optimal k for k-means clustering using the elbow curve method 
"""
class elbowFinder: 
    def __init__(self, k_start, k_end):
        self.k_start = k_start
        self.k_end = k_end 
        self.clusterer = None
    
    
    """
    Displays elbow curve graph to find the optimal value of K 
    The graph is up for interpretation to determine value of K 
    """
    def find_optimal_k(self): 
        SSEs = [] # Sum of squared errors or each value of K 
        k_values = [i for i in range(self.k_start, self.k_end+1)] # Values of K (used for x-axis of graph)
        # For each k, compute the sum of squared errors 
        for k in range(self.k_start, self.k_end+1): 
            # Run k-means for that k 
            self.clusterer = k_means.kMeansClusterer(k, "newData.txt")
            self.clusterer.cluster()
            error = self.calculate_SSE()
            SSEs.append(error)
        # Graph elbow curve 
        plt.plot(k_values, SSEs)
        plt.xlabel("K")
        plt.ylabel("Sum of Squared Errors")
        plt.title("Elbow Curve Analysis for K-Means Clustering")
        plt.show()
        
        
    """
    Returns the sum of squared errors for a single k-means clustering
    """
    def calculate_SSE(self): 
        centers = self.clusterer.centers
        SSE = 0 
        # Compute distance squared of each point to its centroid, and sum them
        for data_point in self.clusterer.training_data: 
            curr_cluster_center = centers[data_point.cluster]
            # Use euclidean distance 
            dist_sq = math.pow((curr_cluster_center.percent - data_point.percent), 2) + \
                math.pow((curr_cluster_center.volatility - data_point.volatility), 2)
            SSE += dist_sq
        return SSE
    
    
# Uses the elbow curve method to find the optimal k (up to interpretation)
def main(): 
    my_elbow_finder = elbowFinder(2, 12)
    my_elbow_finder.find_optimal_k()

if __name__ == "__main__": 
    main()