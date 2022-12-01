Stock Clustering:

k_means.py
- Runs k-means clustering given a value for k
- To run, manually change the value of k in the code (in main)
- Then run: python3 k_means.py

elbow_method.py
- Runs elbow method for determining optimal k
- To run, manually change the inputs to elbowFinder in main to change the range for k
- Then run: python3 elbow_method.py

silhouette_analysis.py (this one takes a little bit)
- Runs silhouette analysis for determing optimal k
- To run, manually change the inputs to silhouetteMethod in main to change the range fork
- Then run: python3 silhouette_analysis.py

get_sectors.py
- Gets sectors for all tickers 
- Also displays sector information for each cluster 
- To run: python3 get_sectors.py

Other Alterations for K-Means:
- You can turn scaling on and off by commenting out line 54 in k_means.py
- You can run with different seed choices: 
     - Random seed choice: self.initialize_centers_random() 
     - Random data points: self.initialize_centers_with_data()