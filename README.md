yahoo fin documentation:   http://theautomatic.net/yahoo_fin-documentation/#methods

https://algotrading101.com/learn/cluster-analysis-guide/



K-Means 
 1. Read all data from file and create data point: dataPoint(ticker, percent, volitility) into a list 
 2. Create k empty clusters ((list of lists) or (list of maps) ) where each element is a cluster center 
 3. Choose starting point for each cluster center 
 4. Iterate: 
      - assign each data point to closest center 
      - recalculate centers as mean of points in cluster 
 5. Stop on convergence: centers don't change, or when error is less than some value, or after fixed number of iterations 

 Problems to look at: 
  - seed choice: 
      - Random selection 
      - Farthest points heuristic 
      - Try out multiple cluster centers 

Functions to Implement: 
 - func. read_training_data() -> reads data file and creates data points 
 - func. assign_to_centers() -> assigns each data point to the closest center 
 - func. adjust_centers() -> readjusts centers using all data points 
 - func. distance() -> computes distance between center and point (use euclidean)
 - func. display_clusters() -> shows visual representation of clusters 
 - func. find_optimal_k() -> runs k_means for k = 1...n and graphs each (then chooses optimal k)
